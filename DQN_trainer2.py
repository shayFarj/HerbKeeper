
import pygame
import Constants
import Enviroment
from DQN_Agent import DQN_Agent
from ReplayBuffer import ReplayBuffer
from HumanAgent import humanAgent
import torch
import os
import wandb
from pygame.locals import *


MIN_BUFFER = 80


def main():
    #region ###### init ##################
    pygame.init()

    clock = pygame.time.Clock()

    screen = Constants.screen
    main_surf = pygame.Surface(Constants.BOUNDERIES)
    main_surf.fill((0,0,0))

    pygame.display.set_caption("Herb's keeper")

    player = DQN_Agent()
    player_hat = DQN_Agent()
    env = Enviroment.Enviroment(main_surf,player,training=True)
    player.env = env
    player_hat.env = env

    batch_size = 128 #מספר צעדי משחק לאימון אחד
    buffer = ReplayBuffer(path=None) 
    learning_rate = 0.000025 # קצב למידה
    update_hat = 3 #מספר רצף צעדי המשחק שלאחריהן הרשת האחראית לחישוב התגמול העתידי תתעדכן במשקליה ותוספתיה
    epochs = 20000 # מספר משחקים לאסיפת צעדי משחק
    start_epoch = 0 # מספר המשחק ממנו מתחילים את האימון (במקרה של הפסקת האימון באמצע והפעלתו מחדש)
    loss = torch.tensor(0)
    losses = []
    optim = torch.optim.Adam(player.DQN.parameters(), lr=learning_rate)
    # milestones = []

    # for i in range(0,21000*1000,2000*1000):
    #     milestones.append(i)

    # scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,milestones=milestones, gamma=Constants.SCHEDULER_GAMMA)

    #run 11&12&13 is with nerfed game
    #run 15 and above is with new state
    #run 16 is with one herb
    #run 17 is the same as 16 but lower epsilon decay and more extreme rewards
    #run 19 is with less neurons and idle punishing.
    #run 20 added layer of 16 nuerons
    #run 21 fixed state & display, new net
    #run 22 new reward func, more random movement
    #run 23 reward more sensitive, collision reward is less extreme, epsilon decay is lower
    #run 24 new reward func, new method of speed.
    #run 25 using the prev reward func, hoever it uses also reward alpha, and I made it more sensitive.
    #run 26 normalized everthing in state, including reward and punish, boundaries are now cube shaped. no schedualer
    #run 27 net had a useless relu layer after output, which might have screwed with the net. lowered learning rate
    #run 28 is using prev state function
    #run 29 new net, net gets action and state
    #run 30 now using player hat and higher max reward
    #run 31 pushing actual action vectors to buffer (success)
    #run 32 using the eyes state (success)
    #run 33 added bouncer, bouncer is fused with herb in state
    #run 34, bouncer isn't fused, added bouncers move difference to state,a single bouncer has less impact on reward
    #run 35, bouncer has more weight in reward, state and 
    #run 36. a bit less weight for the bouncers
    #run 37 bouncers have less weight, but more weight in collision punish
    #run 38,fixed diff punish and status punish
    #run 39 fixed state func
    #run 40, fixed state func snd added more weight to bouncers
    #run41na added d_relev to reward funx. added more weight to bouncers punish
    #run 42 less weight to bouncers, less epsןמברקilon dec
    #run 43, mincreased delev alpha
    #run 44 fixed punish boun cunx
    #run 45 fixed punish bkun func
    #run 46 increasing epsilon decay
    #run 47 added to relev  alpha
    #run 48 fixed relev_d func
    #run 49 changed punish
    #run 50 rewrofe punish constants
    #run 51 changed relev alpha more biggrr
    #run 52 make bouncerd more harsh and have more weight
    #run 53 bouncers are less harsh, but have mode weight
    #run 54 fixed relev_d func and increased relev alpha, bouncers are less harsh and have less weight
    #run 55 more relev alpha and less scope for bouncers more epsilon decaye
    #run 56 lowered lr and lowered relev alpha
    #run 57 using different relev func, more weight to movement eyes, changed red scope and changed min_status_boun
    #run 58 added more time to survive so agent will have time to learn, changed red scope
    #run 59 changed red scope and lowered time to survive, lowered learning rate
    #run 60 lowered time to survive, changed relev alpha changed herb weight and changed red scope changed the multiplier for movemnet eyes, changed lr
    #run 61, run 61, more movement eyes, movement eyes is positive, status boun is positive,lowered punish alpha, lowered relev alpha 
    #run 62, new relev func, added weight to max_reward, lowered learning rate, added to red scope, epsilon decay greater
    #run 63 lowered punish alpha
    #run 64 bigger red scope
    #run 65 using cuda
    #run 66 using cuda
    run_id = 66# above 7 is with normal 5 is without

    checkpoint_path = f"Data/checkpoint{run_id}.pth"
    buffer_path = f"Data/buffer{run_id}.pth"
    resume_wandb = False
    ######   Checkpoint init ##########
    if os.path.exists(checkpoint_path):
        print("Loading checkpoint" + str(run_id) + "...")
        resume_wandb = True
        checkpoint = torch.load(checkpoint_path)
        start_epoch = checkpoint['epoch']+1
        player.DQN.load_state_dict(checkpoint['model_state_dict'])
        player_hat.DQN.load_state_dict(checkpoint['model_state_dict'])
        optim.load_state_dict(checkpoint['optimizer_state_dict'])
        # scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        buffer = torch.load(buffer_path)
        losses = checkpoint['loss']
        player.DQN.train()
        player_hat.DQN.eval()
        print("Checkpoint loaded!")
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
            # "Schedule": f'{str(scheduler.milestones)} gamma={str(scheduler.gamma)}',
            "epochs": epochs,
            "start_epoch": start_epoch,
            "decay": 0,
            "gamma": Constants.AGENT_GAMMA,
            "batch_size": batch_size,
            "epochs per hat update": update_hat,
            "Model":str(player.DQN),
            "device": str(player.DQN.device)
            }
        )


    #endregion
    render=False
    
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

            action = player.get_action(state,env.spaceship.stuck,epoch=epoch,step=step)
            reward, done , delta = env.move(action=action,events=events,or_delta=1/Constants.FPS,render = render)

            next_state = env.state((1/Constants.FPS)*1000)

            buffer.push(state, Constants.actToEyes(action), torch.tensor(reward, dtype=torch.float32), 
                         next_state, torch.tensor(done, dtype=torch.float32))

            if render:
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
            Q_values = player.DQN(states,actions)
            
            Q_hat_Values = player_hat.DQN(next_states,actions)

            loss = player.DQN.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()
            # scheduler.step()
            #endregion

        
        if epoch % update_hat == 0:
            player_hat.fix_update(dqn=player.DQN)

        print (f'epoch: {epoch} loss: {loss:.2f} LR: {learning_rate} step: {step} time: {1/Constants.FPS*step:.2f} sec fps: {Constants.FPS} epsilon : {player.epsilon_greedy(epoch)}')
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

        
            
        
        if epoch % 300 == 0 and epoch > 0:
            print("Saving checkpoint at : " + str(epoch) + "...")
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': player.DQN.state_dict(),
                'optimizer_state_dict': optim.state_dict(),
                # 'scheduler_state_dict': scheduler.state_dict(),
                'loss': losses,
            }
            torch.save(checkpoint, checkpoint_path)
            torch.save(buffer, buffer_path)
            print("Saved!")

if __name__ == "__main__":
    main()