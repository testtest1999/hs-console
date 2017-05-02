#
# Glassix.py - Examples for creating screenshots for glassix
#
from hs import unity as _unity

def setup():
    import hs
    # reset the studio to blank
    hs.reset()
    # set the camera settings to be favorable to transparent screenshots
    hs.configsetup()

def create_female(name):
    from hs import HSFemale
    hsfem = HSFemale(name)
    if not hsfem.can_create():
        return
    if not hsfem.create():
        return
    return hsfem
    
def play_actions(hsfem = None):
    import hs
    if hsfem == None:
        hsfem = hs.get_first_active_female()
    elif isinstance(hsfem, str):
        hsfem = create_female(hsfem)
        
    if isinstance(hsfem, hs.HSFemale):
        hsfem.reset()
        
        #All clothes on
        hsfem.enable_clothes(0)
        yield True
        
        # loads related animations by character name 
        aplayer = hsfem.load_personality('Strict')
        yield True
        
        for name in aplayer.names:
            aplayer.play(name)  # names available in aplayer.names
            yield True
            
        hsfem.set_mood('angry')
        
        hsfem.set_hand_position('l', 'dummy')
        hsfem.set_hand_position('r', 'goo') #fist
        
    yield None

   
def play_actions(hsfem, rootname, moodmap, clothset):
    import os, time
    import hs
    import UserData, YS_Assist
    from collections import OrderedDict as od
    from UnityEngine import Time
    
    if hsfem == None:
        hsfem = hs.get_first_active_female()
    elif isinstance(hsfem, str):
        hsfem = create_female(hsfem)
    if not isinstance(hsfem, hs.HSFemale):
        yield None
        
    hsfem.reset()
    
    _path = os.path.abspath(os.path.join(UserData.Create("cap"), rootname))
    
    aplayer = None
    for cloth,clothes in clothset.iteritems():
        for k,v in clothes.iteritems():
            if k == 'clothes': 
                hsfem.apply_clothes(v)
                hsfem.enable_clothes(0)
            elif k == 'state': 
                hsfem.enable_clothes(v)
            elif k == 'acc': 
                hsfem.enable_accessories(v)
                
        for mood, states in moodmap.iteritems():
            _subdir = os.path.join(_path, mood)
            if not os.path.exists(_subdir): os.makedirs(_subdir)
            fname = os.path.join(_subdir, cloth + ".png")
            
            # speed up time so captures dont miss
            oldTimeScale = Time.timeScale
            Time.timeScale = 5.0
            try:
                for k,v in states.iteritems():
                    if k == 'persona': 
                        if not aplayer or aplayer.personality != v:
                            aplayer = hsfem.load_personality(v)
                    elif k == 'action':
                        if aplayer: aplayer.play(v)
                    elif k == 'mood':
                        hsfem.set_mood(v)
            finally:
                Time.timeScale = oldTimeScale
            
            yield fname
       
    yield None

def capture_mother(hsfem = None, test=False):
    import hs, time
    from collections import OrderedDict as od
    
    hsfem = hs.HSFemale.create_female('[GX] Mother', attach=True)
    if not hsfem: 
        return None
    
    moodmap = {
            'normal':   od(persona='Strict',    action='Normal Wait', mood='normal'   ), 
            'angry':    od(persona='Strict',    action='Hate',        mood='angry'    ), 
            'sad':      od(persona='Strict',    action='Hate 2',      mood='sad'      ), 
            'happy':    od(persona='Strict',    action='Lewd',        mood='happy'    ), 
            'hypno':    od(persona='Withdrawn', action='Normal Wait', mood='hypno'    ), 
            'surprised':od(persona='Boyish',    action='Like',        mood='surprised'),
            }
            
    clothset = {
            'bath':     od(clothes='Bath Towel',       acc=0, ),
            'casual':   od(clothes='G|Mother Casual',  acc=1, ),
            'naked':    od(clothes='G|Mother Casual',  acc=0, state=2),
            'swimsuit': od(clothes='G|Orange Swim',    acc=0, ),
            'underwear':od(clothes='G|Black Lace',     acc=1, ),
            'work':     od(clothes='G|Mother Work',    acc=1, ),
        }
        
    from UnityEngine import Time
    oldTimeScale = Time.timeScale
    Time.timeScale = 5.0
    try:
        actions = play_actions(hsfem, 'mother', moodmap, clothset)
        while True:
            fname = actions.next()
            if not fname: break
            print fname
            time.sleep(0.5)
            if not test:
                hs.capture(fname)
    finally:
        Time.timeScale = oldTimeScale
    # scene = od(clothset['naked'], moodmap['surprised'])
    
    
def cap_mother_scenes(test=False):
    import hs, time
    # hs.reset(); hs.configsetup()

    def cap_scenes():
        import hs, os.path, UserData

        _path = os.path.abspath(os.path.join(UserData.Create("cap"), 'mother'))
        if not os.path.exists(_path): os.makedirs(_path)
        
        # surprise
        hs.move_camera(pos=(0.0, 0.9, 0.0), dir=(0.0, 0.0, -5.0), angle=(8.5, 184.4, 0.0), fov=23.0)
        # begin females
        hsfem = hs.HSFemale.create_female('[GX] Mother', attach=True)
        #hsfem.load_animation('adv/00.unity3d', 'adv_f_01_00')
        hsfem.play_ik('G Cover')
        hsfem.move(pos=(0.0, 0.0, 0.0), rot=(0.0, 0.0, 0.0))
        hsfem.chara.SetActiveTop(True)
        hsfem.chara.ChangeBlinkFlag(False)
        hsfem.chara.ChangeEyesPtn(11,True)
        hsfem.chara.ChangeMouthPtn(7,True)
        hsfem.chara.ChangeLookNeckPtn(3)
        hsfem.chara.ChangeLookEyesPtn(1)
        hsfem.set_clothes_state_all(2)
        hsfem.enable_accessories(0)
        yield os.path.join(_path,'dailybath (1).png')
        
        hs.move_camera(pos=(-0.5, 1.0, 0.0), dir=(0.0, 0.0, -3.8), angle=(24.5, 193.4, 0.0), fov=23.0)
        hsfem.reset()
        #hsfem.load_animation('adv/00.unity3d', 'adv_f_07_00')
        hsfem.play_ik('G Bath Step')
        hsfem.move(pos=(-0.5, -0.3, 0.0), rot=(359.2, 129.0, 359.4))
        hsfem.chara.ChangeBlinkFlag(False)
        hsfem.chara.ChangeEyesPtn(1,True)
        hsfem.chara.ChangeMouthPtn(1,True)
        hsfem.chara.ChangeLookNeckPtn(5)
        hsfem.chara.ChangeLookEyesPtn(1)
        hsfem.set_clothes_state_all(2)
        hsfem.enable_accessories(0)
        # begin items
        item = hs.HSItem.create_item('Bathtub (Yellow)', attach=True)
        item.move(pos=(0.2, -0.1, 0.0), rot=(0.0, 23.0, 4.0))
        yield os.path.join(_path,'dailybath (2).png')
        
        hs.move_camera(pos=(-0.4, 0.5, -0.1), dir=(0.0, 0.0, -3.5), angle=(34.0, 157.1, -1.8), fov=23.0)
        # begin females
        hsfem.reset()
        hsfem.load_animation('custom/cf_anim_custom.unity3d', 'edit_F')
        hsfem.play_ik('G Sit Bath 2')
        hsfem.move(pos=(0.0, 0.2, -0.6), rot=(359.7, 7.1, 1.0))
        hsfem.chara.ChangeBlinkFlag(True)
        hsfem.chara.ChangeEyesPtn(5,True)
        hsfem.chara.ChangeMouthPtn(1,True)
        hsfem.chara.ChangeLookNeckPtn(3)
        hsfem.chara.ChangeLookEyesPtn(0)
        hsfem.set_clothes_state_all(2)
        hsfem.enable_accessories(1)
        # begin items
        item = hs.HSItem.create_item('Bathtub (Yellow)', attach=True)
        item.move(pos=(0.0, 0.0, 0.0), rot=(0.0, 0.0, 0.0))
        yield os.path.join(_path,'dailybath (3).png')

        yield None
    
    # accelerate time to avoid awkward captures
    from UnityEngine import Time
    oldTimeScale = Time.timeScale
    Time.timeScale = 5.0
    try:
       
        scenes = cap_scenes()
        for scene in scenes:
            if not scene: break
        
            print scene
            time.sleep(2.5)
            if not test:
                hs.capture(scene)
    
    finally:
        Time.timeScale = oldTimeScale
    
def cap_sister_scenes(attach=False, test=False):
    import os.path
    # sister bath surprise
    import hs, time
    if not attach:
        hs.reset(); hs.configsetup()

    def cap_scenes():
        import hs, os.path, UserData

        _path = os.path.abspath(os.path.join(UserData.Create("cap"), 'sister'))
        if not os.path.exists(_path): os.makedirs(_path)
            
        hs.move_camera(pos=(0.0, 0.8, 0.0), dir=(0.0, 0.0, -2.3), angle=(21.9, 169.7, 0.0), fov=23.0)
        # begin females
        hsfem = hs.HSFemale.create_female('[GX]Sister', attach=True)
        hsfem.load_animation('h/anim/female/00.unity3d', 'ha_f_02')
        hsfem.move(pos=(0.0, 0.1, -0.6), rot=(7.4, 3.2, 356.0))
        hsfem.chara.SetActiveTop(True)
        hsfem.chara.ChangeBlinkFlag(False)
        hsfem.chara.ChangeEyesPtn(28,True)
        hsfem.chara.ChangeMouthPtn(16,True)
        hsfem.chara.ChangeLookNeckPtn(1)
        hsfem.chara.ChangeLookEyesPtn(1)
        hsfem.set_clothes_state_all(2)
        # begin items
        item = hs.HSItem.create_item('Bathtub (Yellow)')
        item.move(pos=(0.0, 0.0, 0.0), rot=(0.0, 0.0, 0.0))
        yield os.path.join(_path,'dailybath (3).png')
        
        yield None
    
    # accelerate time to avoid awkward captures
    from UnityEngine import Time
    oldTimeScale = Time.timeScale
    Time.timeScale = 5.0
    try:
    
        scenes = cap_scenes()
        for scene in scenes:
            if not scene: break
            print scene
            time.sleep(2.5)
            if not test:
                hs.capture(scene)
                
    finally:
        Time.timeScale = oldTimeScale
        
def run(test=False):
    setup()
    capture_mother(test=test)
    cap_mother_scenes(test=test)
    cap_sister_scenes(test=test)
