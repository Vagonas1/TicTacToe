# TODO Add welcome menu
# TODO Add Player vs Player button on menu 
# TODO Add Player vs CPU button on menu


import pygame 

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
                            if score[index] == 0:
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
                    
                    
        # display menu, buttons and text
        text1 = font.render("Play", True, (255, 255, 255))
        text2 = font.render("Quit", True, (255, 255, 255))
        text_rect1 = text1.get_rect(center=(200, 275))
        text_rect2 = text2.get_rect(center=(290, 275))
        
        # display text and buttons
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), button1)
        pygame.draw.rect(screen, (255, 0, 0), button2)
        screen.blit(text, text_rect)
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        screen.blit(text, text_rect)
        pygame.display.flip()
    
    return running


if __name__ == "__main__":
    main()
