
from embeddings import Embeddings


class BlockTTS():

    def __init__(self, corefs, iT, model, sents):
        self.corefs = corefs
        #print(corefs)
        self.iT = iT
        self.embeddings = Embeddings(model)
        self.sents = sents
        self.them = self.getThem(iT.levels)
        self.maxchars = 420
        self.thresh = 0.6
        self.buildBlocks()

    
    def getThem(self, levels):
        # This list includes a dictionary of themLabels and text spans included in each sentence as well as the full sentence.
        ## {'T1': 'This service', 'R1': 'is good', 'fullsent': 'This service is good'}
        ### I added a new key 'prog_type' to be filled in when the progression type is computed
        # This output is saved as self.them 
        thems = []

        for sentIdx, lvl in enumerate(levels):
            them = lvl[0]
            dthem = {}
            dthem["components"] = []
            for start, end, themLabel in them:
                substr = " ".join(self.sents[sentIdx][start-1:end])
                dthem["components"].append((start, end,themLabel))
                dthem[themLabel] = substr
                #print('------------')
                #print('them variable', them)
            

            dthem["tokens"] = self.sents[sentIdx]
            dthem["fullsent"] = " ".join(self.sents[sentIdx])
            dthem["prog_type"] = ''
            thems.append(dthem)
        #print('==================')
        #print('Function getThem output')
        #print('==================')
        #print('thems variable:', thems)

        return thems


    def check_corefs(self, lastThem, currentThem):
        
        for corefList in self.corefs:
            foundTc = False
            foundTl = False
            foundRl = False
            for corefElem in corefList:
                if "T1" in lastThem:
                    if corefElem in lastThem["T1"].lower():
                        foundTl = True
                        #print("found in last theme", corefElem)
                if "T1" in currentThem:
                    if corefElem in currentThem["T1"].lower():
                        foundTc = True
                        #print("found in current theme", corefElem)
                if "R1" in lastThem:
                    if corefElem in lastThem["R1"].lower():
                        fountRl = True
                        #print("found in last rheme", corefElem)

            if foundTl and foundTc:
                return 'continuous'
            elif foundTc and foundRl:
                return 'linear'

        return 'simple'

    def check_sim(self, lastThem, currentThem):
        
        vectorTl = None
        vectorTc = None
        vectorRl = None
        if "T1" in lastThem:
            tokens = lastThem["T1"].split()
            if len(tokens) > 1:
                vectorTl = self.embeddings.getMsgVector(lastThem["T1"])
                
        if "T1" in currentThem:
            tokens = currentThem["T1"].split()
            if len(tokens) > 1:
                vectorTc = self.embeddings.getMsgVector(currentThem["T1"])
                
        if "R1" in lastThem:
            tokens = lastThem["R1"].split()
            if len(tokens) > 1:
                vectorRl = self.embeddings.getMsgVector(lastThem["R1"])
                
                
        if vectorTc and vectorTl:
            sim = self.embeddings.distance(vectorTc, vectorTl)
            #print(currentThem["T1"],"|||",lastThem["T1"], sim)
            if sim < self.thresh:
                return 'continuous'

        if vectorTc and vectorRl:
            sim = self.embeddings.distance(vectorTc, vectorRl)
            #print(currentThem["T1"],"|||", lastThem["R1"], sim)
            if sim < self.thresh:
                return 'linear'
        
        return 'simple'

    def string_match(self, lastThem, currentThem):
        if "T1" in currentThem:
            if "T1" in lastThem and currentThem["T1"].lower() in lastThem["T1"].lower():
                return 'continuous'
            if "R1" in lastThem and currentThem["T1"].lower() in lastThem["R1"].lower():
                return 'linear'

        return 'simple'

    def need_to_merge(self, lastThem, currentThem):
        test1 = self.string_match(lastThem, currentThem)   

        if test1 != 'simple':
            return test1
        else:
            test2 = self.check_corefs(lastThem, currentThem)
            if test2 != 'simple':
                return test2
            else:
                test3 = self.check_sim(lastThem, currentThem)
                return test3


    def buildBlocks(self):
        # UPDATE MD: blocks and self.blocks contained raw text for ouput in the blockTTS tab
        # I have modified this variable to pass the whole information to ouput thematic progression
        ## This info is the one stored in self.them, but grouped in blocks
        # The logic to ouput the thematic progression in the frontend is implemented in this version.
        
        length = 0
        blocks = []
        currentBlock = []
        lastThem = None

        themblocks = []
        currThemBlock = []

        for themDict in self.them:
            #print("currentBlock", currentBlock)
            #print("blocks",blocks)

            if lastThem:
                if len(themDict["fullsent"]) >= self.maxchars:
                    #print("sentence is too large, we skip this one")
                    pass
                else:
                    if length + len(themDict["fullsent"]) < self.maxchars:
                        prog = self.need_to_merge(lastThem, themDict)
                        themDict["prog_type"] = prog
                        
                        if prog != 'simple':
                            #print("-------------we merge------------")
                            currentBlock.append(themDict)
                            length = length + len(themDict["fullsent"])
                        
                        else:
                            #print("---------creating new block---------")
                            if currentBlock:
                                blocks.append(currentBlock)
                                currentBlock = []
            
                            currentBlock.append(themDict)
                            length = len(themDict["fullsent"])

                    else:
                        #print("char limit reached. current size: ", length, "with new sent", length + len(themDict["fullsent"]))
                        blocks.append(currentBlock)
                        currentBlock = []
                        themDict["prog_type"] = 'simple'
                        currentBlock.append(themDict)
                        length = len(themDict["fullsent"])
            else:
                themDict["prog_type"] = 'simple'
                currentBlock.append(themDict)
                length = length + len(themDict["fullsent"])

            lastThem = themDict
        
        blocks.append(currentBlock)
        #print('xxxxxxxx')
        #print(blocks)
        self.blocks = blocks



