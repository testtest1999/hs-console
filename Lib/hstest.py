from hs import unity as _unity
from hs import translate

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
    
def setup():
    import hs
    import time
    
    # reset the studio to blank
    hs.reset()
    
    # set the camera settings to be favorable to transparent screenshots
    setupconfig()
    
    hs.move_camera(pos=(0.0, 0.9, 0.0), dir=(0.0, 0.0, -5.0), angle=(0.0, 180.1, 0.0), fov=23.0)
    
    #for name, fname in get_charname_list('female'):
    #    print "%20s %s"%(name, fname)
    #for name, fname in get_charname_list('male'):
    #    print "%20s %s"%(name, fname)

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
    
def play_actions(hsfem = None, rootname='mother'):
    import os, time
    import hs
    import UserData, YS_Assist
    from collections import OrderedDict as od
    from UnityEngine import Time
    
    if hsfem == None:
        hsfem = hs.get_first_active_female()
    elif isinstance(hsfem, str):
        hsfem = create_female(hsfem)
    if isinstance(hsfem, hs.HSFemale):
        hsfem.reset()
        
        #All clothes on
        #hsfem.enable_clothes(0)
        #yield True
        _path = os.path.abspath(os.path.join(UserData.Create("cap"), rootname))
        
        moodmap = {
                'normal':   od(persona='Strict',    action='Normal Wait', mood='normal'   ), 
                'angry':    od(persona='Strict',    action='Hate',        mood='angry'    ), 
                'sad':      od(persona='Strict',    action='Hate 2',      mood='sad'      ), 
                'happy':    od(persona='Strict',    action='Lewd',        mood='happy'    ), 
                'hypno':    od(persona='Withdrawn', action='Normal Wait', mood='hypno'    ), 
                'surprised':od(persona='Boyish',    action='Like',        mood='surprised'),
                }
        clothset = {
                'bath':     od(name='Bath Towel',       acc=0, ),
                'casual':   od(name='G|Mother Casual',  acc=1, ),
                'naked':    od(name='G|Mother Casual',  acc=0, state=2),
                'swimsuit': od(name='G|Orange Swim',    acc=0, ),
                'underwear':od(name='G|Black Lace',     acc=1, ),
                'work':     od(name='G|Mother Work',    acc=1, ),
            }
        
        aplayer = None
        for cloth,clothes in clothset.iteritems():
            for k,v in clothes.iteritems():
                if k == 'name': 
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
                print fname
                time.sleep(0.5)
                hs.capture(fname)
                
                yield True

        # loads related animations by character name 
        
        #for name in aplayer.names:
        #    aplayer.play(name)  # names available in aplayer.names
        #    yield True
            
        #hsfem.set_mood('angry')
        #hsfem.set_hand_position('l', 'dummy')
        #hsfem.set_hand_position('r', 'goo') #fist
        
    yield None
        
def run():
    import hs
    import time
    from Manager import Studio
    studio = Studio.Instance
    setup()
    hsfem = create_female('[GX] Mother')
    if not hsfem: 
        return None
    return play_actions(hsfem)
    
    
def runall():
    itr = run()
    while(itr.next()): time.sleep(1)
    
    

def load_excel_data(abdataPath, loader, bundle = 'abdata'):
    import ExcelData
    from collections import OrderedDict
    from System import Int32
    import AssetBundleManager
    from AnimationDataManager import _AnimationDataManager__ExcelCovert as ExcelCovert
    from AnimationDataManager import AnimationData
    list = []
    result = OrderedDict()
    operation = AssetBundleManager.LoadAllAsset(abdataPath, ExcelData, bundle)
    if not operation:
        return result
        
    print 'Getttings assets'
    for data in operation.GetAllAssets[ExcelData]():
        if not data: continue
        
        print 'reading sheets'
        if (data.name.IndexOf('Sheet1') != -1):
            list = []
            for param in data.list:
                if (param.list.Count > 0):
                    ok, num2 = Int32.TryParse(param.list.Item[0])
                    if ok: list.append(ExcelCovert(param))
        elif (data.name.IndexOf('Sheet2') != -1):
            for covert in list:
                list2 = data.Get(covert.start, covert.end)
                for j in range(list2.Count):
                    param2 = list2.Item[j]
                    if (param2.list.Count > 0):
                        ok, _ = Int32.TryParse(param2.list.Item[0])
                        if ok:
                            name, data = loader(param2)
                            result[name] = data
    return result
    
def load_items():
    import StudioItemManager
    import hs
    def loader(param):
        data = StudioItemManager.ItemDataLoader.Item(param)
        name = hs.translate(data.name)
        return (name, data)
        
    abdataPath = r'studio/list/itemlist/honey/sbpr_basutabu_list.unity3d'
    return load_excel_data(abdataPath, loader, bundle='abdata')
    

def ListAnimationFileName():
    import GlobalMethod
    from System.IO import Directory
    
    import UserData
    import os.path
    from System.IO import DirectoryInfo
    hFolder = os.path.join('studio','list','h')
    
    for i in range(0,4):
        text = GlobalMethod.LoadAllListText(hFolder, 'AnimationInfo_studio_%02d'%i)
        if not text: continue
        print text
        matrix = GlobalMethod.GetListString(text)
        if not matrix or matrix.GetLength(0) == 0:
            continue
        for j in range(0, matrix.GetLength(0)):
            name = matrix.GetValue(j,0)
            if not name: continue
            name = hs.translate(name)                
            id = int(matrix.GetValue(j,1))
            assetpathMale = matrix.GetValue(j,2)
            fileMale = matrix.GetValue(j,3)
            assetpathFemale = matrix.GetValue(j,9)
            fileFemale = matrix.GetValue(j,10)
            
            print name, id, assetpathMale, fileMale, assetpathFemale, fileFemale 
    
def bath_scene():
    pass
    
    
def test():
    import hs
    hs.reset(); hs.configsetup()
    hs.move_camera(pos=(0.0, 0.8, 0.0), dir=(0.0, 0.0, -2.3), angle=(21.9, 169.7, 0.0), fov=23.0)
    # begin females
    hsfem = hs.HSFemale.create_female('[GX]Sister')
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

def get_names():   
    import ClothesStateKindFemale
    clothes = hsfem.chara.femaleClothes
    names = Enum.GetNames[ClothesStateKindFemale]()
    for i in range(0,len(names)):
        IsStateKind(4)
        self.SetClothesState(i, state)

def cleanup():
    import unity_util
    unity_util.clean_behaviors()
    

def behavior_test():
    import unity_util
    import UnityEngine
    from UnityEngine import GUI, GUILayout, Screen, Rect, Input, KeyCode, WaitForSeconds
    import System
    unity_util.clean_behaviors()
    
    class DemoMessage():
        def __init__(self):
            self.color = UnityEngine.Color.white
            self.counter = 1
            self.options = System.Array.CreateInstance(UnityEngine.GUILayoutOption, 0)
            self.show_buttons = False
            self.gameObject = None # will be assigned if exists as member
            self.component = None # will be assigned if exists as member
            self.visible = True
            #print "Called when object is created"
            
        def Update(self):
            # Update is called less so better place to check keystate
            if Input.GetKeyDown(KeyCode.F8):
                # unity sucks for checking meta keys
                ctrl, alt, shift = unity_util.metakey_state()
                if ctrl and not alt and not shift:
                    self.visible = not self.visible
                    
        def OnGUI(self):
            if self.visible:
                #self.counter = self.counter + 1
                origColor = GUI.color
                try:
                    GUI.BeginGroup(Rect (Screen.width / 2 - 50, Screen.height / 2 - 50, 400, 400))
                    GUI.color = self.color
                    with GUILayout.VerticalScope("Group", GUI.skin.window):
                        GUILayout.Label(str(self.counter))
                        self.show_buttons = GUILayout.Toggle(self.show_buttons, "Buttons")
                        if self.show_buttons:
                            if GUILayout.Button("Click me"):
                                print "clicked"
                            if GUILayout.Button("Slow Timer"):
                                self.component.StartCoroutine( self.RunSlowTimer() )
                            if GUILayout.Button("Close"):
                                if self.gameObject: 
                                    UnityEngine.Object.DestroyObject(self.gameObject)
                except:
                    GUI.color = origColor
                GUI.EndGroup()
                
        def RunSlowTimer(self):
            for i in range(1,10):
                self.counter = self.counter + 1
                yield WaitForSeconds(1)
            yield None
            
            
        def __del__(self):
            #print "Called when object is garbage collected"
            pass
    
    return unity_util.create_gui_behavior(DemoMessage)