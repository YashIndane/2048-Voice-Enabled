import speech_recognition as SR
from itertools import compress 
import collections
import pygame
import random
import sys
import time



#..................................Colours and property settings.........................................#

RECOG = SR.Recognizer()
pygame.init()

DARK_GREY , LIGHT_GREY = (132 , 132 , 132) , (153 , 153 , 153)
White , Black , Font_style = (255 , 255 , 255) , (0 , 0 , 0) , 'Eras Bold ITC'

font  = pygame.font.SysFont(Font_style , 64)
font2 = pygame.font.SysFont(Font_style , 52) 
font3 = pygame.font.SysFont(Font_style , 40)
font_score = pygame.font.SysFont(Font_style , 28)
font_line  = pygame.font.SysFont(Font_style , 25)
font_2048  = pygame.font.SysFont(Font_style , 100)
label_2048 = font_2048.render('2048' , 1 , DARK_GREY)
label_line = font_line.render('Play voice enabled 2048 game' , 1 , DARK_GREY)
label_line2 = font_line.render('Join the numbers and get to the 2048 tile!' , 1 , DARK_GREY)
label_win = font_2048.render('You win!' , 1 , White)
label_go = font_2048.render('Game over!' , 1 , White)
label_score = font_line.render('SCORE' , 1 , White)
label_real_score = font_line.render('0' , 1 , White)


label_dict = {
               'label_2'   : font.render('2' ,    1 , Black) , 'label_4'   : font.render('4' ,     1 , Black),
               'label_8'   : font.render('8' ,    1 , White) , 'label_16'  : font.render('16' ,    1 , White),
               'label_32'  : font.render('32' ,   1 , White) , 'label_64'  : font.render('64' ,    1 , White),
               'label_128' : font2.render('128' , 1 , White) , 'label_256' : font2.render('256' ,  1 , White),
               'label_512' : font2.render('512' , 1 , White) , 'label_1024': font3.render('1024' , 1 , White),
               'label_2048': font3.render('2048', 1 , White)
             }

labels_positions = []

tile_col_dict = {
                   'tilecolor_2'    : (210 , 210 , 210), 'tilecolor_4'   : (255 , 242 , 229),
                   'tilecolor_8'    : (255, 173 , 96)  , 'tilecolor_16'  : (255 , 127, 80),
                   'tilecolor_32'   : (255 , 99 , 71)  , 'tilecolor_64'  : (255 , 0 , 0),
                   'tilecolor_128'  : (250 , 218 , 94) , 'tilecolor_256' : (255 , 213 , 0),
                   'tilecolor_512'  : (254 , 208 , 0)  , 'tilecolor_1024': (244 , 188 , 28),
                   'tilecolor_2048' : (246 , 211 , 20)
                }

screen , ball_count = pygame.display.set_mode((450 , 600)) , 1
tile_size , precise = 89 , 96.95


a , b = [36 , 133 , 230 , 327] , [183 , 280 , 377 , 474]
positions = [[data_a , data_b] for data_a in a for data_b in b]
idx_array = list(range(16))

tile_info_array , h_vals = [] , []
Real_Pos_Val = [] 

command_dict   = { 'north' : 'y -= 1' , 'south' : 'y += 1' ,
                   'left'  : 'x -= 1' , 'right' : 'x += 1' }

gap_decision   = { 'north' : 'tile_info_array[0][0][1] < h' , 'south' : 'tile_info_array[0][0][1] > h' , 
                   'left'  : 'tile_info_array[0][0][0] < h' , 'right' : 'tile_info_array[0][0][0] > h' }  

boundary_check = { 'north' : 'len(V := set(Real_Pos_Val).intersection(set(east_west[0])))   > 0' , 
                   'south' : 'len(V := set(Real_Pos_Val).intersection(set(east_west[3])))   > 0' ,
                   'left'  : 'len(V := set(Real_Pos_Val).intersection(set(north_south[0]))) > 0' , 
                   'right' : 'len(V := set(Real_Pos_Val).intersection(set(north_south[3]))) > 0' ,
                 } 

boundary_check_old = { 'north' : 'temp_y == 183' , 'south' : 'temp_y == 474',
                       'left'  : 'temp_x == 36'  , 'right' : 'temp_x == 327'} 

north_south = [[0 , 1 , 2 , 3]  , [4 , 5 , 6 , 7]  , [8 , 9 , 10 , 11] , [12 , 13 ,14 , 15]]  
east_west   = [[0 , 4 , 8 , 12] , [1 , 5 , 9 , 13] , [2 , 6 , 10 , 14] , [3 , 7 , 11 , 15]]  

#.......................................Function-Definations..............................................#

def create_playarena() :
    m , n = 36 , 183
    pygame.draw.rect(screen , DARK_GREY , [ 26 , 174 , 400 , 400])
    for _ in range(4) :
         for _ in range(4) :
             pygame.draw.rect(screen , LIGHT_GREY ,[m , n , tile_size , tile_size])
             m += 97
         m = 36 
         n += 97 
    
    pygame.display.update() 

def generate_next_tile(P) :
    
    label_ran = random.random()
    ran_idx = random.choice(list(set(idx_array) - set(P)))
    a_ , b_ = positions[ran_idx]
    Real_Pos_Val.append(positions.index([a_ , b_]))
    
    x_2 , y_2 =  a_ + int(tile_size/2) - 10 , b_ + int(tile_size/2) -20
    label = label_dict.get('label_2') if label_ran < 0.85 else label_dict.get('label_4')
    labels_positions.append([label , [x_2 , y_2] , ran_idx])
    t_c = tile_col_dict.get('tilecolor_2') if label == label_dict.get('label_2') else tile_col_dict.get('tilecolor_4')
    pygame.draw.rect(screen , t_c , [a_ , b_ , tile_size , tile_size])
    tile_info_array.append([[a_ , b_] , t_c])

    screen.blit(label, (x_2 , y_2))

    pygame.display.update()

def update_K(X , movement , rem) -> list : 
     temp = []
     temp_dict = {'left' : -4 , 'right' : 4 , 'north' : -1 , 'south' : 1}
     for Ke in X : temp.append(Ke if positions[Ke] in rem else Ke + temp_dict.get(movement))
     return temp

def update_h_value(T , M) :
    h_vals.clear() 
    temp_dict1 = {'left' : [0 , -precise] , 'right' : [0 , precise] , 'north' : [1 , -precise] , 'south' : [1 , precise]}
    for data in T : h_vals.append(data[temp_dict1.get(movement)[0]] + temp_dict1.get(movement)[1])

def create_scoreboard() : 
    pygame.draw.rect(screen , LIGHT_GREY ,[274 , 35 , 110 , 53 ]) 
    screen.blit(label_score , (300 , 42))
    screen.blit(label_real_score , (325 - adjust , 65))

def endgame(T , score) -> bool :  
    T1 = (246 , 211 , 20) in [E[1] for E in T]
    T2 = len(T) == 16
    if T1 or T2 : 
        time.sleep(3)
        screen.fill(Black)
        screen.blit(label_win if T1 else label_go , (80 , 100))
        label_fin_sc = font_score.render('Your score : ' + str(score) , 1 , White)
        screen.blit(label_fin_sc , (142 , 200))
        pygame.display.update()
        time.sleep(8)
        return False
    else : return True  

create_playarena()
screen.blit(label_2048  , (26 , 30))
screen.blit(label_line  , (26 , 110))
screen.blit(label_line2 , (26 , 135))
pygame.draw.rect(screen , LIGHT_GREY , [274 , 35 , 110 , 53 ])
screen.blit(label_score , (300 , 42))
screen.blit(label_real_score , (325 , 65))

x , y = positions[random.choice(idx_array)]
pygame.draw.rect(screen , tile_col_dict.get('tilecolor_2') , [x , y , tile_size , tile_size] ) 
screen.blit(label_dict.get('label_2') , (x + int(tile_size/2) - 10 , y + int(tile_size/2) -20))
tile_info_array.append([[x , y] , tile_col_dict.get('tilecolor_2')]) 
Real_Pos_Val.append(positions.index([x , y])) 
    
pygame.display.update()

x_1 , y_1 = x + int(tile_size/2) - 10 , y + int(tile_size/2) -20
labels_positions.append([label_dict.get('label_2') , [x_1 , y_1] , positions.index([x , y])])
score , status = 0 , True

#...........................................Main-Game-Loop...............................................#

while(status) :

    with SR.Microphone() as source :

        for event in pygame.event.get():
             if (event.type == pygame.QUIT) : sys.exit()
        
        RECOG.adjust_for_ambient_noise(source)

        print('say command ....')

        audio = RECOG.listen(source)

        try :  
            movement = RECOG.recognize_google(audio)

            if movement in command_dict.keys():

                print(f'the command given : {RECOG.recognize_google(audio)}')

                #only keep which are eligible to move in 1st level checking
                remove = []
                temp_dict4 = {'left'  : north_south[0] , 'right' : north_south[3],
                              'north' : east_west[0]   , 'south' : east_west[3]}
                              
                remove = [u[0] for u in tile_info_array if positions.index(u[0]) in temp_dict4.get(movement)]
                

                #second level checking
                temp_dict5 = {'left' : 4 , 'right' : -4 , 'north' : 1 , 'south' : -1}
                
                for data in remove :
                        u = positions.index(data) + temp_dict5.get(movement)
                        for _ in range(3) : 
                            try : 
                              if positions[u] in [_w_[0] for _w_ in tile_info_array] : 
                             
                                remove.append(positions[u])
                                u += temp_dict5.get(movement)
                              
                              else : break
                            except : pass 

                _e_ = [positions.index(c) for c in remove]

                grid_value_LR = []

                for _i_ in range(4) :
                    try  : 
                        qq , temp = _i_ , []
                        for _j_ in range(4) :
                            for _zz_ , _xx_ , _yy_ in labels_positions :
                                if _yy_ == qq : 
                                    temp.append([_zz_ , _yy_])
                                    break
                            qq += 4
                    except : pass        
                    grid_value_LR.append(temp)

                 
                grid_value_NS_N = []
                for gr in range(4) :
                    temp__ = [] 
                    for ii in range(3 , -1 , -1) :
                        try : temp__.append(grid_value_LR[ii][gr])
                        except : pass
                    grid_value_NS_N.append(temp__)       
                       
                
                grid_value_NS_S = [_p_[::-1] for _p_ in grid_value_NS_N]

                grid_value_LR_L = [_f_[::-1] for _f_ in grid_value_LR]
                
            
                remove_list = []
                grid_dict_all = {'right' : grid_value_LR    ,  'left' : grid_value_LR_L ,
                                 'north' : grid_value_NS_N  , 'south' : grid_value_NS_S}

                 
                for _h_ in list(grid_dict_all.get(movement)) : 
                    my_set = set()
                    for _p_ in range(len(_h_) - 1) : 

                        if _h_[_p_][0] == _h_[_p_ + 1][0] :
                             remove_list.append(_h_[_p_][1])
                             for _o_ in range(0 , _p_) : my_set.add(_h_[_o_][1])
                    for _n_ in my_set : remove_list.append(_n_)

               
                _e_ = [_E_ for _E_ in _e_ if _E_ not in remove_list]

                positions_rem_list = [positions[i_i] for i_i in _e_]
                      
                    
                flag = True if len(positions_rem_list) <= len(tile_info_array) else False 

                if movement in command_dict.keys() :

                    update_h_value([_z_[0] for _z_ in tile_info_array] , movement)
                    
                    for _ in range(105) :

                        create_playarena()

                        for  COR , COL  in  tile_info_array : 

                            pygame.draw.rect(screen , COL , [COR[0] , COR[1] , tile_size , tile_size]) 
                        
                            pygame.display.update() 

                        exp = list(filter(lambda x : x == movement , command_dict.keys()))[0]


                        tile_move = {'left' : 'POS[0] -= 1' , 'right' : 'POS[0] += 1' , 'north' : 'POS[1] -= 1' , 'south' : 'POS[1] += 1'}
                        
                        
                        for LABEL , POS , IDX in labels_positions : # This block moves all block labels accordingly 
                            t_label = ''
                            for l_k , l_v in label_dict.items() : 
                                if l_v == LABEL : 
                                    t_label = l_k
                                    break

                            if   t_label in ['label_2' , 'label_4' , 'label_8']       : x_r , y_r = 0  , 0  
                            elif t_label in ['label_16' , 'label_32' , 'label_64']    : x_r , y_r = 14 , 0
                            elif t_label in ['label_128' , 'label_256' , 'label_512'] : x_r , y_r = 19 , 4
                            else : x_r , y_r = 22 , 8

                            screen.blit(LABEL , (POS[0] - x_r , POS[1] + y_r))
                            pygame.display.update()
                            if IDX not in _e_ :  exec(tile_move.get(movement))
                                
                            
                        temp_x , temp_y , temp = x , y , []
                    
                        for A , _C_ in tile_info_array :

                            temp_dict3 = {'left' : [A[0] - 1 , A[1]] , 'right' : [A[0] + 1 , A[1]],
                                          'north' :[A[0] , A[1] - 1] , 'south' : [A[0] , A[1] + 1]}
                            
                            temp.append([temp_dict3.get(movement) if A not in positions_rem_list else A , _C_]) 
                                    
                        tile_info_array = temp  
                        
                        x , y = tile_info_array[0][0] 
                        
                        GAP , c = [] , 0
                        for data in [_z_[0] for _z_ in tile_info_array] : 

                            GAP.append(data[0] > h_vals[c] if movement == 'left'  else
                                       data[0] < h_vals[c] if movement == 'right' else 
                                       data[1] > h_vals[c] if movement == 'north' else data[1] < h_vals[c])
                            c += 1

                        if not all(GAP) : break
                    
                        
                    temp_label = []
                    for L__ , P__ , I__ in labels_positions :  
                       I__ -= 0 if I__ in _e_ else temp_dict5.get(movement)
                       temp_label.append([L__ , P__ , I__])
                    labels_positions = temp_label
                           
                status = endgame(tile_info_array , score)
               
                Real_Pos_Val = update_K(Real_Pos_Val , movement , positions_rem_list)

                C_RPV , T_RPV = dict(collections.Counter(Real_Pos_Val)) , []
                for keys in C_RPV.keys() :T_RPV.append(keys)
                Real_Pos_Val = T_RPV
                

                only_idx = [idx_ for la_ , po_ , idx_ in labels_positions]
                rep_idx  = [idx__ for idx__ , count__ in dict(collections.Counter(only_idx)).items() if count__ > 1]

                T_LPO , k_ = [] , []
                for label_ , pos_ , idx_ in labels_positions : 
                   
                        if idx_ in rep_idx :
                            if idx_ not in k_ :  
                                temp_label = 'temp_'
                                for _l_ , _lo_ in label_dict.items() : 
                                    if _lo_ == label_ : 
                                        temp_label = _l_
                                        break

                                digit = int(temp_label[temp_label.index('_') + 1:]) 
                                n_digit = str(digit * 2)
                                
                                T_LPO.append([label_dict.get('label_' + n_digit) , pos_ , idx_])
                                
                                k_.append(idx_) 
                            else : pass

                        else : T_LPO.append([label_ , pos_ , idx_])        
                
                labels_positions = T_LPO

                T_TIA , W_ , l_score = [] , [] , score

                for position , col in tile_info_array : 

                    if position in [positions[a] for a in rep_idx] : 
                        if position not in W_ : 

                            for __n , __m in tile_col_dict.items() : 
                                if __m == col : 
                                    col_label = __n
                                    break

                            digit_col = int(col_label[col_label.index('_') + 1 :]) 
                            new_col_digit = str(digit_col * 2)
                            score += int(new_col_digit)

                            T_TIA.append([position , tile_col_dict.get('tilecolor_' + new_col_digit)])

                            W_.append(position)
                        else : pass
                    else : T_TIA.append([position , col])

                tile_info_array = T_TIA    

                if flag and status : generate_next_tile(Real_Pos_Val)
                
              
                label_real_score = font_line.render(str(score) , 1 , White)
                
               
                len_sc , _q_ = len(str(score)) , 65
                adjust = 0 if len_sc == 1 else 5 if len_sc == 2 else 9 if  len_sc == 3 else 13 if len_sc == 4 else 17
                if status : 
                    if score - l_score != 0 : 
                            for i in range(31) : 
                                create_scoreboard()
                                label_inc = font_line.render('+' + str(score - l_score) , 1 , Black)
                                screen.blit(label_inc , (325 - adjust , _q_))
                                pygame.display.update()
                                _q_ -= 1
                                time.sleep(0.025)
                            
                    create_scoreboard()
                pygame.display.update()
                
               
        except Exception as e : pass     
