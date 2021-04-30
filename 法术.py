from ColorLog import ColorLogDecorator
import time
import random


class card:
    def __init__(self, numb, name, attr, func):
        self.name = name
        self.numb = numb
        self.attr = attr
        self.func = func


class player:
    def __init__(self, symbol, name, locate, buff, hp, defense, armor, tramp, cih):
        self.symbol = symbol
        self.locate = locate
        self.name = name
        self.buff = buff
        self.hp = hp
        self.moveable = False
        self.defense = defense
        self.armor = armor
        self.tramp = tramp
        self.cih = cih


class Game:
    def __init__(self):
        print('欢迎来到《法术大乱斗》')
        print('创意来自传奇工作室')
        print('创新工作室出品')
        print('题材作者:天峰')
        print('开发:Lsamc')
        print('技术支持:Lrjis')
        time.sleep(2)

        ColorLogDecorator.active()
        self.symbol = ['·',
        ColorLogDecorator.yellow('✯', 'strong'),
        ColorLogDecorator.green('✯', 'strong')]
        self.max_hp = 2039
        self.start_defence = 0

        print('\033c', end='')
        print(ColorLogDecorator.white('法术大乱斗', 'bg-strong'))
        self.p = [
            player(self.symbol[1], input('玩家1名字:'), (0, 0), [[0,0], 0, 0, 0], self.max_hp, self.start_defence, [0], [0, []],
                   []),
            player(self.symbol[2], input('玩家2名字:'), (6, 6), [[0,0], 0, 0, 0], self.max_hp, self.start_defence, [0], [0, []],
                   [])]
        print('\033c')
        self.current, self.opposite = 0, 1
        print(ColorLogDecorator.white('%s的回合...'%self.p[self.current].name,'bg-strong'))
        input()
        self.Card = [card(0, '火球术  ', 'fire', self.fireball),
                     card(1, '疾电闪行 ', 'storm', self.flashmove),
                     card(2, '火球术  ', 'fire', self.fireball),
                     card(3, '助燃   ', 'fire', self.助燃),
                     card(4, '助燃   ', 'fire', self.助燃),
                     card(5, '疾电闪行 ', 'storm', self.flashmove),
                     card(6, '旋风斩  ', 'hit', self.旋风斩),
                     card(7, '旋风斩  ', 'hit', self.旋风斩),
                     card(8, '火球术  ', 'fire', self.fireball),
                     card(9, '火球术  ', 'fire', self.fireball),
                     card(10, '火球术  ', 'fire', self.fireball),
                     card(11, '冰锥   ', 'ice', self.冰锥),
                     card(12, '虚弱诅咒 ', 'dark', self.weaken),
                     card(13, '停战协议 ', 'buff', self.silence),
                     card(14, '制导打击 ', 'tech', self.tracemissle),
                     card(15, '传送   ', 'tech', self.portal),
                     card(16, '防备   ', 'tramp', self.beingaware),
                     card(17, '地雷   ', 'tramp', self.mine),
                     card(18, '地雷   ', 'tramp', self.mine),
                     card(20, "无尽剑  ", "armor", self.infinitesword),
                     card(19,'火种   ','fire',self.kindling),
                     card(21,'五连火球术','fire',self.fire_fire)
                     card(22,'冰刺   '，'ice',)]
        
        self.turn = 0
        
        self.end = False
        self.deck = []
        self.discard = []
        self.record=[]
        self.currentcard = len(self.Card)
        for i in range(0, self.currentcard):
            self.deck.append(i)
        random.shuffle(self.deck)
        for i in range(0, 4):
            self.p[0].cih.append(self.deck.pop())
            self.currentcard -= 1
            self.p[1].cih.append(self.deck.pop())
            self.currentcard -= 1
        self.board = dict()
        self.setback()

    def introduce(self):
        print('\033c')
        print('命令：m代表移动')
        print('     p代表结束回合')
        print('     #1代表使用编号1的卡')
        print('蓝色的格点代表可以移动的地方')
        print('红色的格点代表可以攻击的地方')
        print('黄蓝两棋分别代表先后手')
        print('方向：1左上\t2上\t3右上\t')
        print('      4左\t5自己\t6右\t')
        print('      7左下\t8下\t9右下\t')
        print('其他代表取消(取消建议不输入)')
        input()
    def switchside(self):
        self.current, self.opposite = self.opposite, self.current

    def startstage(self):
        if self.p[self.current] == self.p[0]:
            self.turn += 1
        if (not self.p[self.current].buff[1]):
            self.p[self.current].moveable = True
        if self.currentcard <= 1:
            for i in self.discard:
                self.discard.remove(i)
                self.deck.append(i)
                self.currentcard += 1
            random.shuffle(self.deck)
        
        if not len(self.p[self.current].cih)==5:
        	flag=True
            while(flag):
            	a=self.deck.pop()
            	if not a in (20,21):
            	    self.p[self.current].cih.append(a)
                    self.record.append(self.p[self.current].name+'摸了一张牌')
                    flag=False
                else:
                    self.discard.append(a)
                    flag=True
            
        else:
        	a=self.deck.pop()
        	self.discard.append(a)
        	self.record.append(self.p[self.current].name+'摸到并弃置'+self.Card[a].name)
        	print('你因牌数满了，无法获得%s'%self.Card[a].name)
        	input()
        self.currentcard -= 1
        

    def battlestage(self):
        skip = False
        while not skip:
            self.printboard()
            command = input('你的命令？')
            if command == '':
                pass
            else:
                if command[0] == '#':
                    if self.p[self.current].buff[3]:
                        print('你被沉默了，无法出卡')
                        input()
                    else:
                        if int(command[1:]) in self.p[self.current].cih:
                            if self.Card[int(command[1:])].func():
                                if not self.Card[int(command[1:])].attr=='tramp':
                                    self.record.append(self.p[self.current].name+'使用'+self.Card[int(command[1:])].name)
                                else:
                                    self.record.append(self.p[self.current].name+'设置了陷阱')
                                self.p[self.current].cih.remove(int(command[1:]))
                                self.discard.append(int(command[1:]))
                        else:
                            print('你没有该卡')
                            input()
                elif command[0] == 'h':
                    self.introduce()
                elif command[0] == 'm':
                    if self.p[self.current].moveable:
                        if self.move():
                            self.record.append(self.p[self.current].name+'进行了移动')
                            self.p[self.current].moveable = False
                    else:
                        print('你不能移动了')
                        input()
                elif command[0] == 'p':
                    print('结束回合....')
                    skip = True
                    input()
                elif command[0] == 's':
                    print('你投降了...')
                    self.end = True
                    input()
                    print('\033c')
                    print(self.p[self.opposite].name + '获得了胜利✌')
                    exit()
                else:
                    print('无效命令')
                    input()

    def endstage(self):
        self.p[self.current].buff = [0, 0, 0, 0]
        while len(self.p[self.current].cih)>5:
            print('你的牌需弃至五张')
            ca=input('弃置:')
            if ca[0] == '#':
                if int(ca[1:]) in self.p[self.current].cih:
                    self.p[self.current].cih.remove(int(ca[1:]))
                    self.discard.append(int(ca[1:]))
                    self.record.append(self.p[self.current].name+'弃置了'+self.Card[int(ca[1:])].name)
                else:
                    print('你没有该卡')
                    input()
        self.switchside()
        print('\033c', end='')
        print(ColorLogDecorator.white('%s的回合...'%self.p[self.current].name,'bg-strong'))
        input()

    def printboard(self):
        print('\033c', end='')
        print('回合:%d' % self.turn, end='\t')
        print('牌堆还有:%d张牌' % len(self.deck), end='\t')
        print('弃牌堆有%d张牌' % len(self.discard))
        for i in range(0, 7):
            for j in range(0, 7):
                if j==6:print(self.board[(i, j)], end='‖')
                else:print(self.board[(i, j)], end='   ')
            
            d=len(self.record)-13
            if d>0:
                print(self.record[2*i])
            else:
                if not (2*i)>=len(self.record):
                    print(self.record[2*i])
                else:print()
            if not i==6:print('                         ‖',end='')
            else:print('═══════════════╝',end='')
            if d>0:
                print(self.record[2*i+1])
            else:
                if not (2*i+1)>=len(self.record):
                    print(self.record[2*i+1])
                else:print()

        print(self.p[self.current].name + ':HP:%d+%d' % (self.p[self.current].hp, self.p[self.current].defense),
              end='  ')
        if self.p[self.current].armor[0]: print('无尽剑:耐久%d' % self.p[self.current].armor[0], end='  ')
        if self.p[self.current].buff[0][0]: print('助燃%d'%self.p[self.current].buff[0][0], end='  ')
        if self.p[self.current].buff[1]: print('冰冻', end='  ')
        if self.p[self.current].buff[2]: print('弱化%d'%self.p[self.current].buff[2], end='  ')
        if self.p[self.current].buff[3]: print('沉默', end='  ')
        if self.p[self.current].tramp[0]: print(ColorLogDecorator.blue('防备'),end='  ')
        print()
        if len(self.p[self.current].tramp[1]):
            print(ColorLogDecorator.blue('地雷'), end='')
            print(self.p[self.current].tramp[1])

        print(self.p[self.opposite].name + ':HP:%d+%d' % (self.p[self.opposite].hp, self.p[self.opposite].defense),
              end='  ')
        if self.p[self.opposite].armor[0]: print('无尽剑:耐久%d' % self.p[self.opposite].armor[0], end='  ')
        if self.p[self.opposite].buff[0][0]: print('助燃%d'%self.p[self.opposite].buff[0][0], end='  ')
        if self.p[self.opposite].buff[1]: print('冰冻', end='  ')
        if self.p[self.opposite].buff[2]: print('弱化%d'%self.p[self.opposite].buff[2], end='  ')
        if self.p[self.opposite].buff[3]: print('沉默', end='  ')
        print()
        if self.p[self.current].moveable: print('当前可移动，', end='')
        print('你的手牌：')
        j = False
        for i in self.p[self.current].cih:
            if not j:
                print('#%d %s' % (i, self.Card[i].name), end='\t')
                j = True
            else:
                j = False
                print('#%d %s' % (i, self.Card[i].name))
        if j:
            print()

    def setback(self):
        for i in range(0, 7):
            for j in range(0, 7):
                self.board[(i, j)] = self.symbol[0]

        self.board[self.p[0].locate] = self.symbol[1]
        self.board[self.p[1].locate] = self.symbol[2]

    def ifsuccess(self):
        if self.p[self.opposite].hp <= 0:
            self.setback()
            self.printboard()
            print('%s倒在了地上...' % self.p[self.opposite].name)
            input()
            print('\033c')
            print('%s获得了最终的胜利✌' % self.p[self.current].name)
            exit()

    def damagemake(self,damage,attr,*word):
        bu = self.p[self.current].buff
        ar = self.p[self.current].armor
        if damage < 0:
            if ((bu[0][0])&(attr=='fire')):
                self.p[self.current].buff[0][0] = 0
            if ((bu[0][1])&(attr=='storm')):
                self.p[self.current].buff[0][1] = 0
            if len(word):
            	print(word[0])
            return 0
        else:
            if ((bu[0][0])&(attr=='fire')):
                damage += (1+bu[0])
                self.p[self.current].buff[0][0] = 0
            if ((bu[0][1])&(attr=='storm')):
                damage+=1
                self.p[self.current].buff[0][1] = 0
            
            if bu[2]:
                damage -= bu[2]
            if ar[0]:
                damage *= 2
                ar[0] -= 1
                self.p[self.current].armor = ar

            self.record.append(self.p[self.opposite].name+'失去了%dHP因为'%damage)
            if not self.p[self.opposite].defense:self.p[self.opposite].hp -= damage
            else:
            	if(self.p[self.opposite].defense>=damage):
            		self.p[self.opposite].defense-=damage
            	else:
            		self.p[self.opposite].hp-=(damage-self.p[self.opposite].defense)
            		self.p[self.opposite].defense=0
            if len(word):
            	print(word[1])
            self.ifsuccess()
            return 1

    def move(self):
        loc = self.p[self.current].locate
        for i in range(loc[0] - 1, loc[0] + 2):
            for j in range(loc[1] - 1, loc[1] + 2):
                if ((i in range(0, 7)) & (j in range(0, 7)) & (not (loc == self.p[self.opposite].locate))):
                    self.board[(i, j)] = ColorLogDecorator.blue(self.board[(i, j)], 'strong')
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('移动中...')
        dire = input('方向？')
        if dire == '':
            self.setback()
            return 0
        dire = int(dire)
        self.setback()
        if dire == 0:
            return 0
        loc = list(loc)
        if dire in (1, 4, 7): loc[1] -= 1
        if dire in (3, 6, 9): loc[1] += 1
        if dire in (1, 2, 3): loc[0] -= 1
        if dire in (7, 8, 9): loc[0] += 1
        loc = tuple(loc)
        if ((loc[0] in range(0, 7)) & (loc[1] in range(0, 7)) & (not (loc == self.p[self.opposite].locate))):
            self.p[self.current].locate = loc
            if self.p[self.opposite].tramp[0]:
                print('咔哒，触发对方陷阱:防备')
                print('对方护甲增加')
                self.p[self.opposite].defense += 2
                self.p[self.opposite].tramp[0]=0
                input()
            if (loc in self.p[self.opposite].tramp[1]):
                print('咔，轰！')
                print('你中了对方的暗雷！')
                self.p[self.current].hp -= 5
                self.ifsuccess()
                input()
            self.setback()
            return 1
        else:
            return 0

    def fireball(self):
        damage = -1
        loc = self.p[self.current].locate
        for i in range(loc[0] - 4, loc[0] + 5):
            if i in range(0, 7):
                if self.board[(i, loc[1])] == self.p[self.opposite].symbol: self.board[
                    (i, loc[1])] = ColorLogDecorator.red('✯', 'bg-strong')
                self.board[(i, loc[1])] = ColorLogDecorator.red(self.board[i, loc[1]], 'strong')
        for i in range(loc[1] - 4, loc[1] + 5):
            if i in range(0, 7):
                if self.board[(loc[0], i)] == self.p[self.opposite].symbol: self.board[
                    (loc[0], i)] = ColorLogDecorator.red('✯', 'bg-strong')
                self.board[(loc[0], i)] = ColorLogDecorator.red(self.board[loc[0], i], 'strong')
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('火球术！')
        dire = input('方向:')
        if dire == '':
            self.setback()
            return 0
        dire = int(dire)
        if dire == 2:
            if ((self.p[self.opposite].locate[1] == loc[1]) & (
                    self.p[self.opposite].locate[0] in range(loc[0] - 4, loc[0]))):
                damage = 3
        elif dire == 4:
            if ((self.p[self.opposite].locate[0] == loc[0]) & (
                    self.p[self.opposite].locate[1] in range(loc[1] - 4, loc[1]))):
                damage = 3
        elif dire == 8:
            if ((self.p[self.opposite].locate[1] == loc[1]) & (
                    self.p[self.opposite].locate[0] in range(loc[0] + 1, loc[0] + 5))):
                damage = 3
        elif dire == 6:
            if ((self.p[self.opposite].locate[0] == loc[0]) & (
                    self.p[self.opposite].locate[1] in range(loc[1] + 1, loc[1] + 5))):
                damage = 3
        else:
            self.setback()
            return 0

        self.damagemake(damage,'fire')
        self.setback()
        return 1

    def 助燃(self):
        self.p[self.current].buff[0][0] += 1
        self.printboard()
        print('获得助燃buff')
        input()
        return 1

    def flashmove(self):
        if self.p[self.current].buff[1]:
        	print('你被冻住了不能动')
        	return 0
        loc = self.p[self.current].locate
        for i in range(loc[0] - 2, loc[0] + 3):
            if i in range(0, 7):
                self.board[(i, loc[1])] = ColorLogDecorator.blue(self.board[i, loc[1]], 'strong')
        for i in range(loc[1] - 2, loc[1] + 3):
            if i in range(0, 7):
                self.board[(loc[0], i)] = ColorLogDecorator.blue(self.board[loc[0], i], 'strong')
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('闪现！')

        dire = input('方向:')
        dis = input('距离:')
        if ((dire == '') | (dis == '')):
            self.setback()
            return 0
        dire, dis = int(dire), int(dis)
        if not dis in range(1, 3):
            print('距离过长')
            self.setback()
            input()
            return 0
        loc = list(loc)
        if dire == 2:
            loc[0] -= dis
        elif dire == 4:
            loc[1] -= dis
        elif dire == 8:
            loc[0] += dis
        elif dire == 6:
            loc[1] += dis
        else:
            self.setback()
            return 0
        loc = tuple(loc)
        if ((loc[0] in range(0, 7)) & (loc[1] in range(0, 7)) & (not (loc == self.p[self.opposite].locate))):
            self.p[self.current].locate = loc
            self.p[self.current].buff[0][1]=1
            self.setback()
            return 1

    def 旋风斩(self):
        damage = -1
        loc = self.p[self.current].locate
        for i in range(loc[0] - 1, loc[0] + 2):
            for j in range(loc[1] - 1, loc[1] + 2):
                if ((i in range(0, 7)) & (j in range(0, 7))):
                    if self.board[(i, j)] == self.p[self.opposite].symbol:
                        damage = 2
                        self.board[(i, j)] = ColorLogDecorator.red('✯', 'bg-strong')
                    self.board[(i, j)] = ColorLogDecorator.red(self.board[(i, j)], 'strong')
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('旋风斩！')

        self.damagemake(damage,'hit')
        self.damagemake(damage,'hit')
        input()
        self.setback()
        return 1

    def 冰锥(self):
        damage = -1
        loc = self.p[self.current].locate
        for i in range(loc[0] - 3, loc[0] + 4):
            if i in range(0, 7):
                if self.board[(i, loc[1])] == self.p[self.opposite].symbol: self.board[
                    (i, loc[1])] = ColorLogDecorator.red('✯', 'bg-strong')
                self.board[(i, loc[1])] = ColorLogDecorator.red(self.board[i, loc[1]], 'strong')
        for i in range(loc[1] - 3, loc[1] + 4):
            if i in range(0, 7):
                if self.board[(loc[0], i)] == self.p[self.opposite].symbol: self.board[
                    (loc[0], i)] = ColorLogDecorator.red('✯', 'bg-strong')
                self.board[(loc[0], i)] = ColorLogDecorator.red(self.board[loc[0], i], 'strong')
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('冰锥！')
        dire = input('方向:')
        if dire == '':
            self.setback()
            return 0
        dire = int(dire)
        if dire == 2:
            if ((self.p[self.opposite].locate[1] == loc[1]) & (
                    self.p[self.opposite].locate[0] in range(loc[0] - 3, loc[0]))):
                damage = 1
        elif dire == 4:
            if ((self.p[self.opposite].locate[0] == loc[0]) & (
                    self.p[self.opposite].locate[1] in range(loc[1] - 3, loc[1]))):
                damage = 1
        elif dire == 8:
            if ((self.p[self.opposite].locate[1] == loc[1]) & (
                    self.p[self.opposite].locate[0] in range(loc[0] + 1, loc[0] + 4))):
                damage = 1
        elif dire == 6:
            if ((self.p[self.opposite].locate[0] == loc[0]) & (
                    self.p[self.opposite].locate[1] in range(loc[1] + 1, loc[1] + 4))):
                damage = 1
        else:
            self.setback()
            return 0

        if self.damagemake(damage,'buff'):
            self.p[self.opposite].buff[1]=1
            self.record.append(self.p[self.opposite].name+'被冰冻了因为')

        self.setback()
        return 1

    def weaken(self):
        print('弱化！')
        self.p[self.opposite].buff[2] += 1
        self.record.append(self.p[self.opposite].name+'被弱化了因为')
        return 1

    def silence(self):
        print('停战！')
        self.p[self.current].buff[3] = 1
        self.p[self.opposite].buff[3] = 1
        self.record.append('大家被沉默因为')

        return 1

    def tracemissle(self):
        damage = -1
        loc = self.p[self.current].locate
        for i in range(loc[0] - 3, loc[0] + 4):
            for j in range(loc[1] - 3, loc[1] + 4):
                if ((i in range(0, 7)) & (j in range(0, 7))):
                    if self.board[(i, j)] == self.p[self.opposite].symbol: self.board[(i, j)] = ColorLogDecorator.red(
                        '✯', 'bg-strong')
                    self.board[(i, j)] = ColorLogDecorator.red(self.board[(i, j)], 'strong')
        self.board[loc] = self.p[self.current].symbol
        self.printboard()

        print('追踪导弹！')
        dx = input('输入增量行')
        dy = input('输入增量列')
        if ((not dx == '') & (not dy == '')):
            dx, dy = int(dx), int(dy)
            if ((dx in range(-3, 4)) & (dx in range(-3, 4))):
                if ((loc[0] + dx, loc[1] + dy) == self.p[self.opposite].locate):
                    damage = 3
            else:
                self.setback()
                return 0
        else:
            self.setback()
            return 0
        self.damagemake(damage,'hit','啪叽','轰！')
        input()
        self.setback()
        return 1

    def portal(self):
        if self.p[self.current].buff[1]:
        	print('你被冻住了不能动')
        	return 0
        loc = self.p[self.current].locate
        for i in range(loc[0] - 3, loc[0] + 4):
            for j in range(loc[1] - 3, loc[1] + 4):
                if ((i in range(0, 7)) & (j in range(0, 7)) & (not (loc == self.p[self.opposite].locate))):
                    self.board[(i, j)] = ColorLogDecorator.blue(self.board[(i, j)], 'strong')
        self.board[loc] = self.p[self.current].symbol
        self.printboard()

        print('传送！')
        dx = input('输入增量行')
        dy = input('输入增量列')
        if ((not dx == '') & (not dy == '')):
            dx, dy = int(dx), int(dy)
            if ((dx in range(-3, 4)) & (dx in range(-3, 4))):
                loc = list(loc)
                loc[0] += dx
                loc[1] += dy
                loc = tuple(loc)
                if not loc == self.p[self.opposite].locate:
                    self.p[self.current].locate = loc
                    self.setback()
                    return 1
                else:
                    self.setback()
                    return 0
            else:
                self.setback()
                return 0
        else:
            self.setback()
            return 0

    def beingaware(self):
        self.p[self.current].tramp[0] = 1
        return 1

    def mine(self):
        loc = self.p[self.current].locate
        for i in range(loc[0] - 3, loc[0] + 4):
            for j in range(loc[1] - 3, loc[1] + 4):
                if ((i in range(0, 7)) & (j in range(0, 7))):
                    self.board[(i, j)] = ColorLogDecorator.red(self.board[(i, j)], 'strong')
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('地雷！')
        dx = input('输入增量行')
        dy = input('输入增量列')
        if ((not dx == '') & (not dy == '')):
            dx, dy = int(dx), int(dy)
            if not((dx in range(-3,4))&(dy in range(-3,4))):
                self.setback()
                return 0
            loc = list(loc)
            loc[0] += dx
            loc[1] += dy
            loc = tuple(loc)
            if ((loc[0] in range(0, 7)) & (loc[1] in range(0, 7)) & (not (loc == self.p[self.opposite].locate)) & (
            not loc == self.p[self.current].locate)):
                self.p[self.current].tramp[1].append(loc)
                for i in self.p[self.current].tramp[1]:
                    self.board[i] = ColorLogDecorator.red(self.board[i], 'strong')
                self.printboard()
                print('请查看地雷位置')
                input()
                self.setback()
                return 1
            else:
                return 0
        else:
            return 0

    def infinitesword(self):
        self.p[self.current].armor[0] = 3
        print('已装备无尽剑')
        return 1
        
    def fire_fire(self):
        damage = -1
        loc = self.p[self.current].locate
        for i in range(loc[0] - 4, loc[0] + 5):
            if i in range(0, 7):
                if self.board[(i, loc[1])] == self.p[self.opposite].symbol: self.board[
                    (i, loc[1])] = ColorLogDecorator.red('✯', 'bg-strong')
                self.board[(i, loc[1])] = ColorLogDecorator.red(self.board[i, loc[1]], 'strong')
        for i in range(loc[1] - 4, loc[1] + 5):
            if i in range(0, 7):
                if self.board[(loc[0], i)] == self.p[self.opposite].symbol: self.board[
                    (loc[0], i)] = ColorLogDecorator.red('✯', 'bg-strong')
                self.board[(loc[0], i)] = ColorLogDecorator.red(self.board[loc[0], i], 'strong')
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('五连火球术！')
        dire = input('方向:')
        if dire == '':
            self.setback()
            return 0
        dire = int(dire)
        if dire == 2:
            if ((self.p[self.opposite].locate[1] == loc[1]) & (
                    self.p[self.opposite].locate[0] in range(loc[0] - 4, loc[0]))):
                damage = 3
        elif dire == 4:
            if ((self.p[self.opposite].locate[0] == loc[0]) & (
                    self.p[self.opposite].locate[1] in range(loc[1] - 4, loc[1]))):
                damage = 3
        elif dire == 8:
            if ((self.p[self.opposite].locate[1] == loc[1]) & (
                    self.p[self.opposite].locate[0] in range(loc[0] + 1, loc[0] + 5))):
                damage = 3
        elif dire == 6:
            if ((self.p[self.opposite].locate[0] == loc[0]) & (
                    self.p[self.opposite].locate[1] in range(loc[1] + 1, loc[1] + 5))):
                damage = 3
        else:
            self.setback()
            return 0
        
        if damage>0:
        	damage=len(self.p[self.current].cih)-1
        	self.damagemake(damage,'fire')
        self.setback()
        return 1
        
    def kindling(self):
        flag=True
        while flag:
            if self.currentcard <= 1:
           	 for i in self.discard:
           	     self.discard.remove(i)
           	     self.deck.append(i)
           	     self.currentcard += 1
           	     random.shuffle(self.deck)
            a=self.deck.pop()
            self.p[self.current].cih.append(a)
            if self.Card[a].attr=='fire':flag=True
            else:flag=False
            self.currentcard -= 1
            print('你摸到了%s'%self.Card[a].name,end='')
            self.record.append(self.p[self.current].name+'摸到了'+self.Card[a].name)
            input()
        return 1

    def icestamp(self):
        damage = -1
        loc = self.p[self.current].locate
        for i in range(loc[0] - 2, loc[0] + 3):
            if i in range(0, 7):
                if self.board[(i, loc[1])] == self.p[self.opposite].symbol: self.board[
                    (i, loc[1])] = ColorLogDecorator.red('✯', 'bg-strong')
                self.board[(i, loc[1])] = ColorLogDecorator.red(self.board[i, loc[1]], 'strong')
        for i in range(loc[1] - 2, loc[1] + 3):
            if i in range(0, 7):
                if self.board[(loc[0], i)] == self.p[self.opposite].symbol: self.board[
                    (loc[0], i)] = ColorLogDecorator.red('✯', 'bg-strong')
                self.board[(loc[0], i)] = ColorLogDecorator.red(self.board[loc[0], i], 'strong')
        self.board[loc] = self.p[self.current].symbol
        self.printboard()
        print('冰刺！')
        dire = input('方向:')
        if dire == '':
            self.setback()
            return 0
        dire = int(dire)
        if dire == 2:
            if ((self.p[self.opposite].locate[1] == loc[1]) & (
                    self.p[self.opposite].locate[0] in range(loc[0] - 2, loc[0]))):
                damage = 2
        elif dire == 4:
            if ((self.p[self.opposite].locate[0] == loc[0]) & (
                    self.p[self.opposite].locate[1] in range(loc[1] - 2, loc[1]))):
                damage = 2
        elif dire == 8:
            if ((self.p[self.opposite].locate[1] == loc[1]) & (
                    self.p[self.opposite].locate[0] in range(loc[0] + 1, loc[0] + 3))):
                damage = 2
        elif dire == 6:
            if ((self.p[self.opposite].locate[0] == loc[0]) & (
                    self.p[self.opposite].locate[1] in range(loc[1] + 1, loc[1] + 3))):
                damage = 2
        else:
            self.setback()
            return 0
        
        if self.damagemake(damage,'ice'):
            if self.p[self.opposite].buff[1]:
                self.p[self.opposite].hp-=5
                if ((dire==2)&(self.p[self.opposite].locate[0]>0)):
                    self.p[self.opposite].locate[0]-=1
                elif ((dire==4)&(self.p[self.opposite].locate[1]>0)):
                    self.p[self.opposite].locate[1]-=1
                elif ((dire==6)&(self.p[self.opposite].locate[1]<6)):
                    self.p[self.opposite].locate[1]+=1
                elif ((dire==8)&(self.p[self.opposite].locate[0]<6)):
                    self.p[self.opposite].locate[0]+=1
                self.setback()
                self.printboard()
                print('破冰！')
                self.record.append(self.p[self.opposite].name+'被破冰')
                input()
        else:
            self.setback()
        return 1
    
    
                    
game = Game()
while not game.end:
    game.startstage()
    game.battlestage()
    game.endstage()
