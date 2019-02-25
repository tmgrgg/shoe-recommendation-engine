import tkinter as tk
from PIL import Image, ImageTk

from munger import Munger
from recommender import Recommender
from functools import partial

class GUI:

    def __init__(self, master, size=4):
        mngr = Munger()
        df_meta, df_features = mngr.munge()
        
        self.recommender = Recommender(df_features, df_meta)
        
        self.shoes = df_meta['CID']
        
        self.size = size
        self.k = size ** 2
                
        self.master = master
        master.title("shüSPACE")
        
        self.background_image=ImageTk.PhotoImage(Image.open('media/shuspace.jpg'))
        background_label = tk.Label(master, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1, bordermode='outside')

        self.label = tk.Label(master, text="shüSPACE")
        self.label.grid()
        
        self.sq_list = []
        
        
        self.initialize_sqs()
        
        
        self.random_button = tk.Button(self.master, text='Randomize!', command=self.randomize)
        self.random_button.grid(row=self.size//2, column=self.size)
            
            
        # when we update recommendations we'll just iterate through and update
        # each sq_list so that 0 will contain the top rec... 1 will contain the second
        # 2 will contain the third etc.
        
        #so we need to map the buttons to locations like this:
        
        #0   1  4   9
        #2   3  6  11
        #5   7  8  13
        #10 12 14  15

        #etc.
        
        r = 0
        alt = 0
        switch = True
        for x in range(self.k):
            
            if switch:
                i = alt
                j = r
            else:
                i = r
                j = alt
                alt += 1
                
            switch = not switch
                
            self.sq_list[x]['button'].grid(row=i, column=j)
            
            if x + 1 == (r + 1)**2:
                r += 1
                alt = 0
                switch = True

    
    def choose(self, i):
        sqs = self.sq_list
        chosen = sqs[i]
        
        recs = self.recommender.recommend_k(self.k, chosen['cid'])
        tgt_cid = recs['tgt']
        print(tgt_cid)
        rec_cids = recs['recommended']
        
        self._update_sq(sqs[0], tgt_cid)
        
        for i in range(1, self.k):
            if (i < len(rec_cids)):
                sq = sqs[i]
                self._update_sq(sq, rec_cids[i-1])
                
                
    def randomize(self):
        random_cids = self.shoes.sample(self.k)
        for i in range(self.k):
            self._update_sq(self.sq_list[i], random_cids[i])
            

            
    def initialize_sqs(self):
        for i in range(self.k):
            cid_btn_dict = {'button': tk.Button(self.master, command=partial(self.choose, i))}
            self.sq_list.append(cid_btn_dict)
        self.randomize()
                
        
    def _update_sq(self, sq, cid):
        sq['cid'] = cid
        sq['image'] = self._get_img(cid) 
        sq['button'].config(image=sq['image'])
        
        
    def _get_img(self, cid):
        return ImageTk.PhotoImage(self.recommender.get_img(cid))



root = tk.Tk()
my_gui = GUI(root, 5)
root.mainloop()
