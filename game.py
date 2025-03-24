import pygame 
import random 

def main():
    # pygame setup
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Tic-Tac-Toe")
    clock = pygame.time.Clock()
    
    # sprites
    background = pygame.image.load("Assets/X-O_Background.png").convert()
    x_sprite = pygame.image.load("Assets/X-O_XSprite.png").convert_alpha()
    o_sprite = pygame.image.load("Assets/X-O_OSprite.png").convert_alpha()
    
    # sounds 
    x_sound = pygame.mixer.Sound("Assets/blipSelect.wav")
    o_sound = pygame.mixer.Sound("Assets/pickupCoin.wav")
    pygame.mixer.music.load("Assets/music.wav") 
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.7)

    # grid buttons 
    grid = [
        pygame.Rect(166 * col, 166 * row, 166, 166)
        for row in range(3)
        for col in range(3)
    ]
    
    # 1 is X,  2 is O and  0 is unused
    score = [0, 0, 0,
             0, 0, 0, 
             0, 0, 0]
    
    x_score = 0
    o_score = 0
    player = "X" 
    
    # game loop
    running = display_menu(screen)
    opponent = choose_opponent(screen)   
            
    while running:
        # event poll
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
            
            # check which square mouse clicked and update the score
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for index, square in enumerate(grid):
                    if square.collidepoint(mouse_x, mouse_y):
                        if player == "X":
                            if score[index] == 0:
                                score[index] = 1
                                player = "O"
                                x_sound.play()
                        else:
                            if score[index] == 0 and opponent != "CPU":
                                score[index] = 2
                                player = "X"
                                o_sound.play()
        
        # display sprites
        screen.blit(background,(0, 0))
        for box ,i in enumerate(score):
            if i == 1:
                screen.blit(x_sprite, grid[box]) 
            elif i == 2:
                screen.blit(o_sprite, grid[box])
        
        # Check for winner or draw
        winner = check_winner(score)
        if winner: 
            if winner == 1:
                winner = "X" 
                x_score += 1
                display_game_over(screen, winner, x_score, o_score)
                score = reset_score(score)
            
            elif winner == 2:
                winner = "O"
                o_score += 1
                display_game_over(screen, winner,x_score, o_score)
                score = reset_score(score)

        if check_draw(score) and winner == 0:
            display_game_over(screen, winner, x_score, o_score)
            score = reset_score(score)    
                
        # refresh screen
        pygame.display.flip()
        clock.tick(60)
        
        # CPU player
        if opponent == "CPU":
            if player == "O" and 0 in score:
                cpu_choice = cpu_move(score)
                score[cpu_choice] = 2
                o_sound.play()
                player = "X"
        

    pygame.quit()

def check_winner(score):
    winning_combinations = [
        [0, 1, 2],  # Top row
        [3, 4, 5],  # Middle row
        [6, 7, 8],  # Bottom row
        [0, 3, 6],  # Left column
        [1, 4, 7],  # Middle column
        [2, 5, 8],  # Right column
        [0, 4, 8],  # Diagonal
        [2, 4, 6],  # Other diagonal
    ] 
    for combination in winning_combinations:
        if score[combination[0]] == score[combination[1]] == score[combination[2]] != 0:
            return score[combination[0]]  # Return the winning player (1 or 2)
    return 0  # Return 0 if no winner

def check_draw(score):
    return all(s != 0 for s in score) 

def reset_score(score):
    score = [0, 0, 0,
             0, 0, 0, 
             0, 0, 0]
    return score 

def display_game_over(screen, winner, x_score, o_score):
    font = pygame.font.Font(None, 36)
    if winner == "X" or winner == "O":
        text = font.render(f"{winner} wins!", True, (255, 255, 255))
    else:
        text = font.render("Draw!", True, (255, 255, 255))
    
    x_display_score = font.render(f"X : {x_score}", True, (255, 255, 255))
    o_display_score = font.render(f"O : {o_score}", True, (255, 255, 255))
    
    # position text
    text_rect = text.get_rect(center=(250, 230))
    x_dis_rect = x_display_score.get_rect(center=(200, 260))
    o_dis_rect = o_display_score.get_rect(center=(300, 260))

    # display text
    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    screen.blit(x_display_score, x_dis_rect)
    screen.blit(o_display_score, o_dis_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

def display_menu(screen):
    # menu screen
    clock = pygame.time.Clock()
    font = pygame.font.Font((None), 36)
    text = font.render("TicTacToe", True, (255, 255, 255))
    text_rect = text.get_rect(center=(250, 150))
    button1 = pygame.Rect(165, 250, 70, 50)
    button2 = pygame.Rect(255, 250, 70, 50)
    
    # button loop
    running = False
    while not running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return running
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button1.collidepoint(mouse_x, mouse_y):
                    running = True
                if button2.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    return running
                    
                    
        # make menu, buttons and text
        text1 = font.render("Play", True, (255, 255, 255))
        text2 = font.render("Quit", True, (255, 255, 255))
        text_rect1 = text1.get_rect(center=(200, 275))
        text_rect2 = text2.get_rect(center=(290, 275))
        
        # draw text and buttons
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), button1)
        pygame.draw.rect(screen, (255, 0, 0), button2)
        screen.blit(text, text_rect)
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(30) 
        
    return running

def choose_opponent(screen):
	#menu screen 
	clock = pygame.time.Clock()
	font = pygame.font.Font((None), 36) 
	text = font.render("Pick Opponent", True, (255, 255, 255))
	text_rect = text.get_rect(center=(250,150))
	
	# make the two options 
	text1 = font.render("Player vs Player", True, (255, 255, 255)) 
	text2 = font.render("Player vs CPU", True, (255, 255, 255))
	text_rect1 = text1.get_rect(center=(250, 225)) 
	text_rect2 = text2.get_rect(center=(240, 275))  
	
	# button look
	opponent = None 
	while opponent == None:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				if text_rect1.collidepoint(mouse_x, mouse_y):
					opponent = "Player" 
				if text_rect2.collidepoint(mouse_x, mouse_y):
					opponent = "CPU"
		
		# draw the options 
		screen.fill((0, 0, 0)) 
		pygame.draw.rect(screen, (0, 255, 0), text_rect1)
		pygame.draw.rect(screen, (255, 0, 0), text_rect2)
		screen.blit(text, text_rect)
		screen.blit(text1, text_rect1)
		screen.blit(text2, text_rect2)
		pygame.display.flip()
		clock.tick(30)
	
	return opponent 

def get_available_moves(score):
    # Returns a list of available (empty) positions on the board.
    return [i for i in range(9) if score[i] == 0]
   
def check_win_move(score, player):
    # Checks if the given player (1 or 2) has a winning move.
    winning_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    
    for a, b, c in winning_positions:
        if score[a] == score[b] == player and score[c] == 0:
            return c
        if score[a] == score[c] == player and score[b] == 0:
            return b
        if score[b] == score[c] == player and score[a] == 0:
            return a
    return None

def cpu_move(score):
    # Determines the best move for the CPU (player 2).
    cpu_symbol = 2
    player_symbol = 1
    pygame.time.wait(1000)
    
    # 1. Check if CPU can win
    best_move = check_win_move(score, cpu_symbol)
    if best_move is not None:
        return best_move

    # 2. Block the player's winning move
    best_move = check_win_move(score, player_symbol)
    if best_move is not None:
        return best_move

    # 3. Take the center if available
    if score[4] == 0:
        return 4

    # 4. Take one of the corners if available
    for move in [0, 2, 6, 8]:
        if score[move] == 0:
            return move

    # 5. Pick any available move
    return random.choice(get_available_moves(score))

		
if __name__ == "__main__":
    main()