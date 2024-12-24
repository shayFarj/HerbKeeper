#region ############### imports ###################
import pygame
import torch
import Constants
import Enviroment
from DQN_Agent import DQN_Agent
from ReplayBuffer import ReplayBuffer
import os
import wandb
#endregion
MIN_BUFFER = 50
def main ():
    #region ################ init Surface of pyGame #################
    pygame.init()
    
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(Constants.BOUNDERIES)
    main_surf = pygame.Surface(Constants.BOUNDERIES)
    main_surf.fill((0,0,0))

    pygame.display.set_caption("Herb's keeper")


    #endregion

    #region ################ params and models ######################
    
    player = DQN_Agent()
    player_hat = DQN_Agent()
    env = Enviroment.Enviroment(main_surf,player)
    player.env = env
    player_hat.env = env
    player_hat.DQN = player.DQN.copy()
    batch_size = 128
    buffer = ReplayBuffer(path=None)
    learning_rate = 0.002
    ephocs = 200000
    start_epoch = 0
    C, tau = 3, 0.001
    loss = torch.tensor(0)
    avg = 0
    losses = []
    optim = torch.optim.Adam(player.DQN.parameters(), lr=learning_rate)
    # scheduler = torch.optim.lr_scheduler.StepLR(optim,100000, gamma=0.50)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[5000*1000, 10000*1000, 15000*1000, 20000*1000, 25000*1000, 30000*1000], gamma=0.5)
    step = 0
    
    #endregion

    #region ################ checkpoint Load ########################
    num = 400
    checkpoint_path = f"Data/checkpoint{num}.pth"
    buffer_path = f"Data/buffer{num}.pth"
    resume_wandb = False
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
    #endregion
    
    #region ################ Wandb.init #############################
    
    wandb.init(
        # set the wandb project where this run will be logged
        project="Herb_Keeper",
        resume=resume_wandb, 
        id=f'Herb_Keeper {num}',
        # track hyperparameters and run metadata
        config={
        "name": f"Herb_Keeper DDQN {num}",
        "checkpoint": checkpoint_path,
        "learning_rate": learning_rate,
        "Schedule": f'{str(scheduler.milestones)} gamma={str(scheduler.gamma)}',
        "epochs": ephocs,
        "start_epoch": start_epoch,
        "decay": 0,
        "gamma": 0.99,
        "batch_size": batch_size, 
        "C": C,
        "tau":tau,
        "Model":str(player.DQN),
        "device": str(player.DQN.device)
        }
    )
    # wandb.config.update({"Model":str(player.DQN)}, allow_val_change=True)
    
    #endregion 

    #region ################ Main Loop ##############################
    for epoch in range(start_epoch, ephocs):
        
        #region ########### Episode loop - one game loop ############
        env.restart()
        end_of_game = False

        while not end_of_game:
            print (step, end='\r')
            step += 1
            
            #region ############# Play and Sample Environement #########################
            main_surf.fill((0,0,0))
            events = pygame.event.get()
            
            state = env.state()

            action = player.get_action(state=state,epoch=epoch)            
            
            

            reward, done = env.move(action=action,events=events)

            next_state = env.state()
            buffer.push(state, torch.tensor(action, dtype=torch.int64), torch.tensor(reward, dtype=torch.float32), 
                        next_state, torch.tensor(done, dtype=torch.float32))
            if done:
                env.clear()
                break

            state = next_state

        
            pygame.display.update()
            # clock.tick(FPS)
            
            if len(buffer) < MIN_BUFFER:
                continue
            # endregion

            #region ############# Train ################
            if epoch % 10 != 0: #await training after aquiring enough episodes
                continue
            states, actions, rewards, next_states, dones = buffer.sample(batch_size)
            Q_values = player.DQN(states)
            Q_hat_Values = player.DQN(next_states)

            loss = player.DQN.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()
            scheduler.step()
            #endregion
        
        #endregion
        
        #region ########### Update target network ###################
        if epoch % C == 0:
            player_hat.fix_update(dqn=player.DQN)
            # player_hat.soft_update(dqn=player.DQN, tau=tau)
            # player_hat.DQN.load_state_dict(player.DQN.state_dict())
        #endregion
            
        #region ########### Printing and saving #####################
        print (f'epoch: {epoch} loss: {loss:.2f} LR: {scheduler.get_last_lr()} step: {step} ')
        step = 0
        if epoch % 10 == 0:
            losses.append(loss.item())

        if (epoch + 1) % 10 == 0:
            wandb.log ({
                "loss": loss.item(),
            })

        if epoch % 1000 == 0 and epoch > 0:
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': player.DQN.state_dict(),
                'optimizer_state_dict': optim.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'loss': losses,
            }
            torch.save(checkpoint, checkpoint_path)
            torch.save(buffer, buffer_path)
        #endregion
                
    #endregion


# region ################### write on surface function ##############
# def write (surface, text, pos = (50, 20)):
#     font = pygame.font.SysFont("arial", 36)
#     text_surface = font.render(text, True, WHITE, BLUE)
#     surface.blit(text_surface, pos)
# endregion

        
if __name__ == "__main__":
    main()