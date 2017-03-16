from hs import unity as _unity

#Setup configuration to be favorable for screenshots
@_unity
def setupconfig():
    """Setup configuration to be favorable for screenshots"""
    from Manager import Studio
    studio = Studio.Instance
    cfgeff = studio.configEffect_st
    cfgeff.bloomToggle.isOn = False
    cfgeff.vignetteToggle.isOn = False
    cfgeff.sunShaftsToggle.isOn = False
    cfgeff.fogToggle.isOn = False
    cfgeff.depthOfFieldToggle.isOn = False
    #cfgeff.ssaoToggle.isOn = True
    #cfgeff.selfShadowToggle.isOn = True
    
    # Turn off backgrounds
    studio.uiBGChanger.onOffToggle.isOn = False

def set_mood(chara, mood = None):
    chara.SetActiveTop(True) # enable character ???
    chara.ChangeBlinkFlag(False) # disable blink
    chara.ChangeEyesOpen(1.0,True)
    if mood == None:
        chara.ChangeEyesPtn(0,True)
        chara.ChangeMouthPtn(0,True)        
        return
    mood = mood.lower()    
    if mood == 'angry':
        chara.ChangeEyesPtn(21,True)
        chara.ChangeMouthPtn(13,True)
    
    
def dump_char_state(chara):
    print "chara.SetActiveTop(%s)"%(chara.GetActiveTop())
    print "chara.ChangeBlinkFlag(%s)"%(chara.GetBlinkFlag())
    print "chara.ChangeEyesPtn(%s,True)"%(chara.GetEyesPtn())
    print "chara.ChangeMouthPtn(%s,True)"%(chara.GetMouthPtn())
    print "chara.ChangeLookNeckPtn(%s)"%(chara.GetLookNeckPtn())
    print "chara.ChangeLookEyesPtn(%s)"%(chara.GetLookEyesPtn())
    print "chara.SetPosition%s"%(chara.GetPosition())
    print "chara.SetRotation%s"%(chara.GetRotation())
        
def dump_camera_state():
    from UnityEngine import Vector3
    from Manager import Studio
    studio = Studio.Instance
    c = studio.CameraCtrl
    print "hs.move_camera(pos=%s, dir=%s, angle=%s, fov=%s)"%(c.TargetPos, c.CameraDir, c.CameraAngle, c.CameraFov)


def dump_char_ui_state(chara):
    import hs
    stChara = hs.focus_studio_char(chara)
    if not stChara: return

    hand_positions = hs.get_hand_positions()
    lposname = hand_positions[stChara.anmMng.hand_L_Type]
    rposname = hand_positions[stChara.anmMng.hand_R_Type]
    
    print("hs.set_hand_position(chara, 'l', '%s')"%lposname)
    print("hs.set_hand_position(chara, 'r', '%s')"%rposname)
       
def test_face(chara, face):
    import Manager.ADV
    from System import Enum
    from Manager.ADV import FacialExpressionPattern as Face
    if not isinstance(face, Face):
        face = Enum.Parse(Face, face, True)
    Manager.ADV.Instance.SetFacialExpression(chara, face)
    

def run():
    #for name, fname in get_charname_list('female'):
    #    print "%20s %s"%(name, fname)
    #for name, fname in get_charname_list('male'):
    #    print "%20s %s"%(name, fname)
    
    from Manager import Studio
    import hs
    import time
    
    # reset the studio to blank
    hs.reset()
    
    # set the camera settings to be favorable to transparent screenshots
    setupconfig()
    
    studio = Studio.Instance
    hAnime = studio.hAnimeListScrlCtrl
    
    fnamelookup = dict(hs.get_charname_list('female'))
    fname = fnamelookup.get('[GX] Mother', None)
    if fname == None: return

    # load sample girl and make default on h animation
    @_unity
    def createfemale(file):
        studio.SelectSex = 1
        chara = hs.place_char('female', file)
        hAnime.CurrentCharaSet()
        if chara:
            chara.ChangeBlinkFlag(False) # disable blink
            chara.tearsLv = 0 # no tears
            chara.ChangeLookNeckPtn(1) #look at camera
            chara.ChangeLookEyesPtn(1) #stare at camera
        return chara
        
    chara = createfemale(fname)
    hs.move_camera(pos=(0.0, 0.9, 0.0), dir=(0.0, 0.0, -5.0), angle=(0.0, 180.1, 0.0), fov=23.0)
    chara.SetPosition(0.0, 0.0, 0.0)
    chara.SetRotation(0.0, 0.0, 0.0)
    
    #All clothes on
    studio.studioUICharaState.ChangeClothesVisible(0)
    
    # loads related animations by character name 
    aplayer = hs.load_personality(chara, 'Strict')
    aplayer.play('Favor')  # names available in aplayer.names    

    set_mood(chara, 'angry')
    hs.set_hand_position(chara, 'l', 'dummy')
    hs.set_hand_position(chara, 'r', 'goo') #fist

    return chara
    
    