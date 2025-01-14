
import pygame
import Constants
import Enviroment
from DQN_Agent import DQN_Agent
from ReplayBuffer import ReplayBuffer
from HumanAgent import humanAgent
import torch
import os
import wandb

MIN_BUFFER = 60


def main():
    #region ###### init ##################
    pygame.init()

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(Constants.BOUNDERIES)
    main_surf = pygame.Surface(Constants.BOUNDERIES)
    main_surf.fill((0,0,0))

    pygame.display.set_caption("Herb's keeper")

    player = DQN_Agent()
    player_hat = DQN_Agent()
    env = Enviroment.Enviroment(main_surf,player,training=True)
    player.env = env
    player_hat.env = env

    batch_size = 128
    buffer = ReplayBuffer(path=None)
    learning_rate = 0.002
    update_hat = 3
    epochs = 20000
    start_epoch = 0
    loss = torch.tensor(0)
    losses = []
    optim = torch.optim.Adam(player.DQN.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[5000*1000, 10000*1000, 15000*1000, 20000*1000, 25000*1000, 30000*1000], gamma=0.5)

    run_id = 7 # 7 is with normal 5 is without

    checkpoint_path = f"Data/checkpoint{run_id}.pth"
    buffer_path = f"Data/buffer{run_id}.pth"
    resume_wandb = False
    ######   Checkpoint init ##########
    if os.path.exists(checkpoint_path):
        resume_wandb = True
        checkpoint = torch.load(checkpoint_path)
        start_epoch = checkpoint['epoch']+1
        player.DQN.load_state_dict(checkpoint['model_state_dict'])
        player_hat.DQN.load_state_dict(checkpoint['model_state_dict'])
        optim.load_state_dict(checkpoint['optimizer_state_dict'])
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        buffer = torch.load(buffer_path)
        losses = checkpoint['loss']
        player.DQN.train()
        player_hat.DQN.eval()
    ###### WandB init ##################
    wandb.init(
            # set the wandb project where this run will be logged
            project="Herb_Keeper",
            resume=resume_wandb,
            id=f'Herb_Keeper {run_id}',
            # track hyperparameters and run metadata
            config={
            "name": f"Herb_Keeper DDQN {run_id}",
            "checkpoint": checkpoint_path,
            "learning_rate": learning_rate,
            "Schedule": f'{str(scheduler.milestones)} gamma={str(scheduler.gamma)}',
            "epochs": epochs,
            "start_epoch": start_epoch,
            "decay": 0,
            "gamma": 0.99,
            "batch_size": batch_size,
            "epochs per hat update": update_hat,
            "Model":str(player.DQN),
            "device": str(player.DQN.device)
            }
        )


    #endregion
    render=True
    
    for epoch in range(start_epoch,epochs):
        env.restart()
        run = True

        step = 0

        while run:
            #region ############## Sample Environment ###########
            step += 1
            main_surf.fill((0,0,0))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        render = not render
            
            state = env.state((1/Constants.FPS)*1000)

            action = player.get_action(state=state,events=events,epoch = epoch)
            reward, done , delta = env.move(action=action,events=events,or_delta=1/Constants.FPS,render = render)

            next_state = env.state((1/Constants.FPS)*1000)

            buffer.push(state, torch.tensor(action, dtype=torch.int64), torch.tensor(reward, dtype=torch.float32), 
                         next_state, torch.tensor(done, dtype=torch.float32))

            screen.blit(main_surf,(0,0))
            pygame.display.update()
            #clock.tick(Constants.FPS)

            if env.gameOver():
                # env.restart()
                break
            
            if len(buffer) < MIN_BUFFER:
                continue
            #endregion
            #region ##################train##################
            
            states, actions, rewards, next_states, dones = buffer.sample(batch_size)
            Q_values = player.DQN(states)
            Q_hat_Values = player.DQN(next_states)

            loss = player.DQN.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()
            scheduler.step()
            #endregion

        
        if epoch % update_hat == 0:
            player_hat.fix_update(dqn=player.DQN)

        print (f'epoch: {epoch} loss: {loss:.2f} LR: {scheduler.get_last_lr()} step: {step} time: {1/Constants.FPS*step:.2f} sec fps: {Constants.FPS}')
        if epoch % 10 == 0:
            losses.append(loss.item())
        if (epoch + 1) % 10 == 0:
            wandb.log ({
                "loss": loss.item(),
            })
            wandb.log ({
                "time" : ((1/Constants.FPS)*step),
            })
        step = 0

        
            
        
        if epoch % 250 == 0 and epoch > 0:
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': player.DQN.state_dict(),
                'optimizer_state_dict': optim.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'loss': losses,
            }
            torch.save(checkpoint, checkpoint_path)
            torch.save(buffer, buffer_path)

if __name__ == "__main__":
    main()