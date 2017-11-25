import matplotlib.pyplot as plt
import collections
from random import randint
class Protein():
    def __init__(self, sequence):
        # self.q = collections.deque()
        self.sequence = sequence
        # self.index = sequence
        self.initialconformation = [(1, 0) for i in range((len(self.sequence) - 1))]
        # for every in sequence:
        #     self.q.append(every)
        # first = 0
        # count =0
        # idr = 0
        # for i in range(len(sequence)-1):
        #     if sequence[i]==1 and sequence[i+1]==0 :
        #
        #         self.initialconformation[i]=[(0,1)]
        #
        #         # idr ==0
        #         idr = 1-dir
        #         first  = 1
        #
        #
        #     elif sequence[i]==0 and sequence[i+1]==1 and first ==1:
        #         self.initialconformation[i]=[(0,1)]
        #         idr = 1-idr
        #     elif sequence[i]==1:
        #         if idr==0:
        #             self.initialconformation[i] = [(0, 1)]
        #         else:
        #             self.initialconformation[i] = [(0, -1)]

        self.initialpositions, self.initialenergy  = self.fold(self.initialconformation)


    def fold(self, sequ):
        positions = [(0.0,0.0)] #x,y
        check = {}
        check[(0.0,0.0)] = 1
        for link in sequ:
            next_pos = (positions[-1][0] + link[0],positions[-1][1] + link[1])
            if next_pos in check:
                return (None, None)
            else:
                check[next_pos] = 1
                positions.append(next_pos)
        return (positions, self.Energy(positions))

    def Energy(self, positions):
        hydrophobic_position = []
        energy = 0
        for acid_idx in range(len(self.sequence)):
            if self.sequence[acid_idx] == 1:
                hydrophobic_position.append(acid_idx)
        for i in range(len(hydrophobic_position)):
            p1 = positions[hydrophobic_position[i]]
            for j in range(i+1,len(hydrophobic_position)):
                p2 = positions[hydrophobic_position[j]]
                energy += ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)**0.5
        return energy

    # Find a different link than current one.
    def changeLinks(self, currsequence):
        dx = [(0.0,1.0),(1.0,0.0),(0.0, -1.0),(-1.0, 0.0)]
        posibleconformation= []
        for j in range(3):
            if dx[j]!=currsequence:
                posibleconformation.append(dx[j])

        return posibleconformation

    # Generate all links in one conforamation.
    def generatesequ(self, length):
        choices = [(0.0,1.0),(1.0,0.0),(0.0, -1.0),(-1.0, 0.0)]
        res = [(0,0)for i in range(length)]
        for i in range(length):
            res[i] = choices[randint(0,3)]
        return res

    def search(self):

        thelowestnergy = self.initialenergy
        thebestposition = self.initialpositions[:]
        thebestconformation = self.initialconformation[:]
        checkdex = True
        for t in range(500):

            # Initialize searching.
            while True:
                if checkdex:
                    start_sequ = self.initialconformation[:]
                    checkdex = False
                else:
                    start_sequ = self.generatesequ(len(self.sequence) - 1)
                best_pos, lowest_energy  = self.fold(start_sequ)
                if lowest_energy != None:
                    break
            best_sequ = start_sequ[:]
            print "The initial lowestEnergy is: ",lowest_energy

            # Start searching.
            count = 0
            while True:
                old_best_sequ = best_sequ[:]
                for link_idx in range(len(best_sequ)):
                    for alter_link in self.changeLinks(best_sequ[link_idx]):
                        cur_sequ = best_sequ[:]
                        cur_sequ[link_idx] = alter_link
                        cur_pos, cur_energy = self.fold(cur_sequ)
                        count += 1
                        if (cur_energy !=  None) and (cur_energy < lowest_energy):
                            lowest_energy = cur_energy
                            best_pos = cur_pos[:]
                            best_sequ = cur_sequ[:]

                if best_sequ == old_best_sequ:
                    break
            if lowest_energy < thelowestnergy:
                thelowestnergy = lowest_energy
                thebestconformation = best_sequ[:]
                thebestposition = best_pos[:]
            print "For searching", count, "times, lowestEnergy is: ",lowest_energy,best_pos,best_sequ

        #  Render the result
        print "Final result: ",thelowestnergy,thebestconformation,thebestposition
        xs = [x[0] for x in thebestposition]
        ys = [x[1] for x in thebestposition]
        colors = {1: "red", 0: "blue"}
        plt.plot(xs, ys,  c='black', zorder=-1, label = "Dist:" + str(thelowestnergy))
        plt.legend(loc='upper left')
        plt.scatter(xs, ys, c=[colors[amino] for amino in self.sequence])
        plt.show()
        return lowest_energy,best_pos




protein = Protein([0,0,0,0,0,1,1,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1,0,0])
protein.search()

#Final result:  285.388329758 [(1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, 1), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)] [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0), (5.0, 0.0), (6.0, 0.0), (7.0, 0.0), (8.0, 0.0), (8.0, 1.0), (7.0, 1.0), (6.0, 1.0), (5.0, 1.0), (4.0, 1.0), (3.0, 1.0), (3.0, 2.0), (4.0, 2.0), (5.0, 2.0), (6.0, 2.0), (7.0, 2.0), (7.0, 3.0), (6.0, 3.0), (5.0, 3.0), (4.0, 3.0), (3.0, 3.0), (2.0, 3.0), (1.0, 3.0), (1.0, 4.0), (2.0, 4.0), (3.0, 4.0), (4.0, 4.0), (5.0, 4.0), (6.0, 4.0), (7.0, 4.0)]


