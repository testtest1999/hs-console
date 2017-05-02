#import UnityEngine

def _call(func, args=(), **kwargs):
    import coroutine
    coroutine.start_new_coroutine(func, args, kwargs)

def unity(func):
    """ Decorator for wrapping unity calls """
    import functools
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            import coroutine
            if args == None: args=()
            return coroutine.start_new_coroutine(func, args, kwargs)
        except Exception:
            pass
    return wrapper

@unity    
def reset():
    from Manager import Studio
    studio = Studio.Instance
    studio.LoadDefaultSceneFile()

def capture(path=''):
    #from HS.Utility import ScreenShot
    #ScreenShot.PerformCapture()
    import screenshot
    screenshot.capture(path)
    
"""Capture does not use the coroutine which can cause issues with UI"""
def capture_noblock(path=''):
    import screenshot
    screenshot.capture_noblock(path)

    
@unity
def quit():
    from Manager import Scene
    scene = Scene.Instance
    scene.GameEnd(False)

@unity
def configsetup():
    """Setup configuration to be favorable for screenshots"""
    from Manager import Studio
    studio = Studio.Instance
    cfgeff = studio.configEffect_st
    cfgeff.bloomToggle.isOn = False
    cfgeff.vignetteToggle.isOn = False
    cfgeff.sunShaftsToggle.isOn = False
    cfgeff.fogToggle.isOn = False
    cfgeff.depthOfFieldToggle.isOn = False
    cfgeff.ssaoToggle.isOn = True
    cfgeff.selfShadowToggle.isOn = True
    studio.uiBGChanger.onOffToggle.isOn = False # Turn off backgrounds

def get_hand_positions():
    import StudioUICharaState
    return StudioUICharaState.handPtnAnimeName
    
def get_hand_position_index(name):
    import StudioUICharaState
    from System import Array
    try:
        return Array.IndexOf(StudioUICharaState.handPtnAnimeName, name)    
    except:
        return None
    
def translate(value):
    try:
        from UnityEngine import Application
        from UnityEngine.UI import Translation
        from System.Text.RegularExpressions import Regex
        tdict = Translation.TextTranslator._TextTranslator__translationsLv[Application.loadedLevel]
        tval = tdict[value]
        if tval: return tval.Value
        
        tdict = Translation.TextTranslator._TextTranslator__translations
        tval = tdict[value]
        if tval: return tval.Value
        
        for kvp in Translation.TextTranslator._TextTranslator__translationsLvR[Application.loadedLevel]:
            m = Regex.Match(text, kvp.Key)
            if m.Success and (m.Groups.Item[0].Value == text):
                str = m.Result(kvp.Value)
                if str: return str
                break
                
        for kvp in Translation.TextTranslator._TextTranslator__translationsR:
            m = Regex.Match(text, kvp.Key)
            if m.Success and (m.Groups.Item[0].Value == text):
                str = m.Result(kvp.Value)
                if str: return str
                break
    except:
        return value
    
@unity
def move_camera(pos=None, dir=None, angle=None, fov=None):
    from UnityEngine import Vector3
    from Manager import Studio
    studio = Studio.Instance
    if pos:
        if isinstance(pos, tuple) and len(pos) == 3:
            pos = Vector3(pos[0], pos[1], pos[2])
        if isinstance(pos, Vector3):
            studio.CameraCtrl.TargetPos = pos
    if dir:
        if isinstance(dir, tuple) and len(dir) == 3:
            dir = Vector3(dir[0], dir[1], dir[2])
        if isinstance(dir, Vector3):
            studio.CameraCtrl.CameraDir = dir
    if angle:
        if isinstance(angle, tuple) and len(angle) == 3:
            angle = Vector3(angle[0], angle[1], angle[2])
        if isinstance(angle, Vector3):
            studio.CameraCtrl.CameraAngle = angle
    if fov != None:
        studio.CameraCtrl.CameraFov = fov
        
class HSCamera(object):
    def move(self, pos=None, dir=None, angle=None, fov=None):
        move_camera(pos=pos, dir=dir, angle=angle, fov=fov)
        
    @property
    def pos(self):
        from Manager import Studio
        return Studio.Instance.CameraCtrl.TargetPos
        
    @pos.setter
    def pos(self,value):
        move_camera(pos=value)
        
    @property
    def dir(self):
        from Manager import Studio
        return Studio.Instance.CameraCtrl.CameraDir
        
    @dir.setter
    def dir(self,value):
        move_camera(dir=value)
        
    @property
    def rot(self):
        from Manager import Studio
        return Studio.Instance.CameraCtrl.CameraAngle
        
    @rot.setter
    def rot(self,value):
        move_camera(angle=value)
        
    @property
    def fov(self):
        from Manager import Studio
        return Studio.Instance.CameraCtrl.CameraFov
        
    @fov.setter
    def fov(self,value):
        move_camera(fov=value)

    def delta_pos(self, x=None, y=None, z=None):
        from Manager import Studio
        camera = Studio.Instance.CameraCtrl
        v = camera.TargetPos
        v = v + Vector3(x if x else 0, y if y else 0, z if z else 0)
        camera.TargetPos = v
        return camera.TargetPos
        
    def delta_dir(self, x=None, y=None, z=None):
        from Manager import Studio
        camera = Studio.Instance.CameraCtrl
        v = camera.CameraDir
        v = v + Vector3(x if x else 0, y if y else 0, z if z else 0)
        camera.CameraDir = v
        return camera.CameraDir

    def delta_rot(self, x=None, y=None, z=None):
        from Manager import Studio
        camera = Studio.Instance.CameraCtrl
        v = camera.CameraAngle
        v = v + Vector3(x if x else 0, y if y else 0, z if z else 0)
        camera.CameraAngle = v
        return camera.CameraAngle
        
    def dump_script(self):
        print "hs.move_camera(pos=%s, dir=%s, angle=%s, fov=%s)"%(str(self.pos), str(self.dir), str(self.rot), str(self.fov))
        
    @staticmethod
    def dump():
        HSCamera().dump_script()
        
def move_camera_delta_pos(x=None, y=None, z=None):
    from UnityEngine import Vector3
    from Manager import Studio
    studio = Studio.Instance
    studio.CameraCtrl.TargetPos
    studio.CameraCtrl.TargetPos = pos

def get_char_dir(type):
    from UnityEngine import Application
    from os import path
    if type in ('female', 'male'):
        return path.realpath(path.join(Application.dataPath,'..','UserData','chara',type))        
    return None
    
def list_char(type):
    from Manager import Studio
    import os
    charpath = get_char_dir(type)
    if charpath:
        return os.listdir(charpath)
    return None

def get_char_name(filename, chartype):
    import System.IO
    coff = 2 if chartype == 'female' else 0
    with System.IO.File.OpenRead(filename) as f:
        with System.IO.BinaryReader(f) as br:
            f.Position = f.Length - 16
            offset = br.ReadInt32()
            f.Position = offset + 787 + coff
            flen = br.ReadInt32()
            return br.ReadString()

def get_charname_list(chartype):
    from os.path import abspath, join
    cdir = get_char_dir(chartype)
    return [(get_char_name(abspath(join(cdir, fname)), chartype), fname) for fname in list_char(chartype)]
    
@unity
def place_char(type, file):
    from Manager import Studio
    from os import path
    charpath = get_char_dir(type)
    if charpath:
        charfile = path.join(charpath, file)
        if path.exists(charfile):
            studio = Studio.Instance
            if type == 'female':
                studio.SelectSex = 1
                return studio.AddFemale(charfile)
            elif type == 'male':
                studio.SelectSex = 0
                return studio.AddMale(charfile)
    return None

                
def get_anime_folderlist():
    from UnityEngine import Object
    import H_AnimeFolderListScrollController
    a = Object.FindObjectsOfTypeAll(H_AnimeFolderListScrollController)
    return None if len(a) == 0 else a[0]


def get_studio_char_from_char(chara):
    from UnityEngine import Vector3
    from Manager import Studio
    import StudioFemale, StudioMale, StudioChara
    studio = Studio.Instance
    for kvp in studio.AllStudioCharaDic:
        id = kvp.Key
        sc = kvp.Value
        if isinstance(sc, StudioFemale):
            if sc.female == chara:
                return (id, sc)
        elif isinstance(sc, StudioMale):
            if sc.male == chara:
                return (id, sc)
    return (None, None)


def focus_studio_char(chara):
    import StudioChara, CharMale, CharFemale
    from Manager import Studio
    studio = Studio.Instance
    if isinstance(chara, (CharFemale,CharMale)):
        id, schar = get_studio_char_from_char(chara)
        if id == None: return None
        chara = schar
    if isinstance(chara, StudioChara):
        studio.SetCurrentCharaController(chara)
    if isinstance(chara, StudioChara): 
        return chara
    return None
    
@unity
def set_hand_position(chara, hand, pos):
    from Manager import Studio
    studio = Studio.Instance
    hand_pos = get_hand_positions()
    if isinstance(pos, int):
        pos = hand_pos[pos]
    if pos not in hand_pos: 
        print pos
        return
    stChara = focus_studio_char(chara)    
    if hand.lower() in ('left', 'l'):
        stChara.hand_L.Play(pos,1)
    elif hand.lower() in ('right', 'r'):
        stChara.hand_R.Play(pos,1)

        
    
def animation_data_run(abdataPath):
    import ExcelData
    from collections import OrderedDict
    from System import Int32
    import AssetBundleManager
    from AnimationDataManager import _AnimationDataManager__ExcelCovert as ExcelCovert
    from AnimationDataManager import AnimationData
    list = []
    result = OrderedDict()
    operation = AssetBundleManager.LoadAllAsset(abdataPath, ExcelData, None)
    if not operation:
        return result
        
    for data in operation.GetAllAssets[ExcelData]():
        if not data: continue
        
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
                            data2 = AnimationData(param2, False)
                            name = translate(data2.name)
                            result[name] = data2
    return result
    
def get_animations():
    _anim = globals().get('_anim')
    if not _anim: 
        from Manager import Studio
        from collections import OrderedDict, namedtuple
        studio = Studio.Instance
        Animations = namedtuple('Animations', 'm, f')
        def load_dict(d):
            o = OrderedDict()
            for df in d.AnimationDataFolderPathList:
                name = translate(df.Value.name)
                abdataPath = df.Value.abdataPath
                o[name] = animation_data_run(abdataPath)
            return o
            
        
        #studio.anmDataFolderMgn_F
        _anim = Animations(m=load_dict(studio.anmDataFolderMgn_M), f=load_dict(studio.anmDataFolderMgn_F))
        globals()['_anim'] = _anim
    return _anim

@unity
def disable_ik():
    from Manager import Studio
    ik = Studio.Instance.studioUIIK
    ik.IK_EnableChange(False)
    ik.IK_EffectorViewChange(False)
    ik.UpdateIKUI()

def get_ik_list():
    import UserData
    import os.path
    from System.IO import DirectoryInfo
    di = DirectoryInfo(os.path.abspath(os.path.join(UserData.Path, "IKPose")))
    return [x.Name for x in di.GetFiles()]
    
def play_ik(stChara, name):
    from Manager import Studio
    from System.IO import File
    import os.path
    import UserData
    
    ik = Studio.Instance.studioUIIK
    fpath = os.path.abspath(os.path.join(UserData.Path, "IKPose", name))
    
    if not File.Exists(fpath):
        return
    @unity
    def run(ik, chara, name, path):
        oldChara = ik.currentSC
        try:
            #ik.currentName
            #ik.currentNameText.text = name
            ik.fileNameIF.text = name
            ik.currentSC = chara
            ik.IK_EnableChange(True)
            ik.Load(path)
            ik.IK_EffectorViewChange(False)
            ik.UpdateIKUI()
        finally:
            ik.currentSC = oldChara
    run(ik,stChara,name,fpath)
    
    
@unity
def load_animation(chara, assetbundle, animation):
    import CharMale, CharFemale
    if not assetbundle or not animation:
        return
        
    if isinstance(chara, (CharMale, CharFemale)):
        chara.LoadAnimation(assetbundle, animation)
    
@unity
def load_personality(chara, personality):
    import Manager
    import StudioFemale, StudioMale, CharMale, CharFemale
    charatype = 'm'
    if isinstance(chara, (CharFemale, StudioFemale)):
        charatype = 'f'
        
    anim = get_animations()
    animdict = getattr(anim, charatype)
    _personaList = animdict.keys()
    _personaMap = dict((y.lower(),x) for x,y in enumerate(_personaList))
    
    if not isinstance(personality, int):
        personality = _personaMap.get(str(personality).lower(), None)
    if personality == None: return
    stChara = focus_studio_char(chara)
    persona = _personaList[personality]

    adv = Manager.ADV.Instance
    ok, ai = adv.animeInfo.TryGetValue(personality)
    if ok and ai:
        disable_ik()
        chara.LoadAnimation(ai.assetbundle, ai.file)
        
    ai = animdict.get(persona, None)
    if ai:
        class AnimationPlayer(object):
            def __init__(self, owner, personality, map):
                self._owner = owner
                self.names = ai.keys()
                self._map = map
                self.personality = _personaList[personality]
                
            def play(self, animation):
                if isinstance(animation, int):
                    animation = self.names[animation]
                data = self._map.get(animation, None)
                if data:
                    @unity
                    def run(owner, data):
                        disable_ik()
                        owner.ChangeAnime(data,0)
                    run(self._owner, data)
                return animation
                
            def play_ik(self, name):
                play_ik(self.owner, name)
                
        # now that personality is loaded.  Addition animations are available in base list
        return AnimationPlayer(stChara, personality, ai)
        
    return None


# load sample girl and make default on h animation
@unity
def createfemale(file):
    chara = place_char('female', file)
    if chara:
        chara.ChangeBlinkFlag(False) # disable blink
        chara.tearsLv = 0 # no tears
        chara.ChangeLookNeckPtn(3) #animation
        chara.ChangeLookEyesPtn(1) #stare at camera
    return chara

@unity
def set_focus_in_hanime():
    """Set Currently Focused Studio Character as default participant in H Animation"""
    from Manager import Studio
    studio = Studio.Instance
    hAnime = studio.hAnimeListScrlCtrl
    hAnime.CurrentCharaSet()

@unity
def set_mood(chara, mood = None):
    #chara.SetActiveTop(True) # enable character ???
    chara.ChangeBlinkFlag(False) # disable blink
    chara.ChangeEyesOpen(1.0,True)
    if mood == None:
        chara.ChangeEyesPtn(0,True)
        chara.ChangeMouthPtn(0,True)        
        chara.ChangeLookNeckPtn(3) #animation
        chara.ChangeLookEyesPtn(1) #stare at camera
        return
        
    eyes, eyelook, mouth, necklook = {
        'normal':       ( 1, 1,  0, 3),
        'angry':        (21, 1, 13, 3),
        'sad':          (10, 1,  9, 3),  
        'happy':        (28, 1,  1, 3),  
        'hypno':        ( 0, 0,  6, 0),  
        'surprised':    (11, 1,  7, 3),
    }.get(mood.lower(), ( 0, 1,  0, 3))
    
    chara.ChangeEyesPtn(eyes,True)
    chara.ChangeLookEyesPtn(eyelook) #stare at camera
    chara.ChangeMouthOpen(False)
    chara.ChangeMouthPtn(mouth,True)
    chara.ChangeLookNeckPtn(necklook) #animation

def list_clothes(sex):
    import FolderAssist, UserData, CharFileInfoClothesMale, CharFileInfoClothesFemale
    import os.path
    from Manager import Studio
    import glob
    from collections import OrderedDict
    
    studio = Studio.Instance
    if sex in ('m','f'):
        sex = 'male' if sex == 'm' else 'female'
    if sex not in ('male','female'):
        return []
    items = OrderedDict()
    for itempath in glob.glob(os.path.join(UserData.Path, 'coordinate', sex, '*.png')):
        clothes = CharFileInfoClothesMale() if sex == 'male' else CharFileInfoClothesFemale()
        clothes.Load(itempath, True)
        clothes.comment = translate(clothes.comment)
        items[clothes.comment] = clothes
    return items

def get_first_active_female():
    from Manager import Studio
    studio = Studio.Instance
    for kvp in studio.femaleList:
        if kvp.Value.body and kvp.Value.female:
            hsfem = HSFemale()
            hsfem.attach(kvp.Value.female)
            return hsfem
    return None

    
    
class HSObject(object):
    def __init__(self, name=None):
        from Manager import Studio
        studio = Studio.Instance
        self.studio = studio
        self.type = None
        self.name = name
        self.chara = None # CharFemale
        self.stChara = None # StudioFemale
        
    def focus(self):
        stChara = focus_studio_char(self.chara)
        if self.stChara == None:
            self.stChara = stChara
        return (stChara != None)
        
    def delete(self):
        if self.stChara:
            if self.focus():
                self.stChara.Delete()
        self.stChara = None
        self.chara = None


    def move(self, pos=None, rot=None):
        if not self.stChara: return False
        
        from UnityEngine import Vector3
        if pos:
            if isinstance(pos, tuple) and len(pos) == 3:
                pos = Vector3(pos[0], pos[1], pos[2])
            self.stChara.objCtrl.transform.localPosition = pos
            
        if rot:
            if isinstance(rot, tuple) and len(rot) == 3:
                rot = Vector3(rot[0], rot[1], rot[2])
            self.stChara.objCtrl.transform.localEulerAngles = rot
        return True
        
    @property
    def pos(self):
        return self.stChara.objCtrl.transform.localPosition
        
    @pos.setter
    def pos(self,value):
        self.move(pos=value)
    
    @property    
    def rot(self):
        return self.stChara.objCtrl.transform.localEulerAngles
        
    @rot.setter
    def rot(self,value):
        self.move(rot=value)
        
    def delta_pos(self, x=None, y=None, z=None):
        from UnityEngine import Vector3
        self.set_pos( self.pos + Vector3(x if x else 0, y if y else 0, z if z else 0) )
        
    def delta_rot(self, x=None, y=None, z=None):
        from UnityEngine import Vector3
        self.set_rot( self.rot + Vector3(x if x else 0, y if y else 0, z if z else 0) )
        
    def __str__(self):
        return self.name
        
        
class HSFemale(HSObject):
    clothes = list_clothes('female')
    
    def __init__(self, name=None, fname=None, chara=None):
        HSObject.__init__(self, name)
        
        from Manager import Studio
        studio = Studio.Instance
        self.type = 'female'
        self.name = name
        if fname == None:
            fnamelookup = dict(get_charname_list('female'))
            self.fname = fnamelookup.get(name, None)
        else:
            self.fname = fname
        self.studio = studio
        self.chara = chara # CharFemale
        self.stChara = None # StudioFemale
        self.aplayer = None # AnimePlayer
        if chara:
            self.name = chara.customInfo.name
            self.fname = chara.chaFile.charaFileName
            ok, stChara = get_studio_char_from_char(chara)
            if ok: self.stChara = stChara
        
    @staticmethod
    def first():
        from Manager import Studio
        studio = Studio.Instance
        for kvp in studio.femaleList:
            if kvp.Value.body and kvp.Value.female:
                hsfem = HSFemale()
                hsfem.attach(kvp.Value.female)
                return hsfem
        return None
        
    def create(self):
        if self.fname and self.chara and self.stChara:
            return True
        self.chara = createfemale(self.fname)
        if not self.chara:
            return False
        self.reset()
        self.focus()
        return self
        
    @staticmethod
    def create_female(name, attach=False):
        if attach:
            hsfem = HSFemale.attach_female(name)
            if hsfem: return hsfem
        return HSFemale(name).create()
        
    @staticmethod
    def attach_female(name):
        from Manager import Studio
        studio = Studio.Instance
        for kvp in studio.femaleList:
            chara = kvp.Value.female
            if kvp.Value.body and chara and chara.customInfo.name == name:
                hsfem = HSFemale()
                hsfem.attach(chara)
                return hsfem
        return None

    def attach(self, chara):
        self.chara = chara
        self.stChara = None
        if chara:
            self.name = chara.customInfo.name
            self.fname = chara.chaFile.charaFileName
            ok, stChara = get_studio_char_from_char(chara)
            if ok: self.stChara = stChara
        self.aplayer = None
        
    def can_create(self):
        import os.path
        if self.fname:
            charpath = get_char_dir(self.type)
            if charpath:
                charfile = os.path.join(charpath, self.fname)
                return os.path.exists(charfile)
        return False
        
    def hanime_focus(self):
        if self.focus():
            set_focus_in_hanime()
        
    # def move(self, pos=None, rot=None):
    #     if not self.chara: return False
    #     
    #     from UnityEngine import Vector3
    #     if pos:
    #         if isinstance(pos, tuple) and len(pos) == 3:
    #             pos = Vector3(pos[0], pos[1], pos[2])
    #         self.chara.SetPosition(pos)
    #     if rot:
    #         if isinstance(rot, tuple) and len(rot) == 3:
    #             rot = Vector3(rot[0], rot[1], rot[2])
    #         self.chara.SetRotation(rot)
    #     return True

    def reset(self):
        chara = self.chara
        if chara:
            chara.ChangeBlinkFlag(False) # disable blink
            chara.tearsLv = 0 # no tears
            chara.ChangeEyesPtn(0,True)
            chara.ChangeMouthPtn(0,True)
            chara.ChangeLookNeckPtn(3) #animation
            chara.ChangeLookEyesPtn(1) #stare at camera
            chara.SetPosition(0,0,0)
            chara.SetRotation(0,0,0)
            set_hand_position(chara, 'l', 0)
            set_hand_position(chara, 'r', 0)
        if self.stChara:
            self.stChara.ikCtrl.IK_Enable(False)
            

    def enable_clothes(self, mode=0):
        if self.focus():
            self.studio.studioUICharaState.ChangeClothesVisible(mode)
            
    def load_personality(self, persona=None):
        if persona == None:
            persona = self.chara.customInfo.personality
        self.aplayer = load_personality(self.chara, persona)
        return self.aplayer
        
    def set_mood(self, mood = None):
        if not self.chara: return False
        return set_mood(self.chara, mood)
        
    def play_ik(self, name):
        play_ik(self.stChara, name)

    def set_hand_position(self, hand, pos=0):
        if not self.chara: return False
        return set_hand_position(self.chara, hand, pos)

    def enable_accessories(self, state):
        """enable all accessories"""
        if not self.chara: return False
        if isinstance(state, (list, tuple)):
            for i, value in enumerate(state):
                self.chara.statusInfo.showAccessory[i] = value
        else:
            self.chara.femaleClothes.SetAccessoryStateAll(state)
        return True
        
    def enable_clothes_state(self, state):
        """enable all clothes state"""
        if not self.chara: return False
        if state != None: return False
        self.chara.femaleClothes.SetClothesStateAll(state)
        return True
        
    def get_clothes(self):
        return HSFemale.clothes
        
    def apply_clothes(self, item):
        import CharFileInfoClothesFemale
        if not item: return
        
        if isinstance(item, CharFileInfoClothesFemale):
            item = item
        elif isinstance(item, int):
            item = HSFemale.clothes[ HSFemale.clothes.keys()[item] ]
        else:
            item = HSFemale.clothes[item]
        if isinstance(item, CharFileInfoClothesFemale):
            @unity
            def run(chara, item):
                chara.femaleClothesInfo.Copy(item)
                chara.Reload()
            run(self.chara, item)
                   
    def load_animation(self, assetbundle, animation):
        import CharMale, CharFemale
        if not assetbundle or not animation:
            return
        load_animation(self.chara, assetbundle, animation)

    def set_clothes_state_all(self, state):
        self.chara.femaleClothes.SetClothesStateAll(state)
        
    def set_clothes_state(self, states):
        clothes = self.chara.femaleClothes
        for i, state in enumerate(states):
            clothes.SetClothesState(i, state)
        
    def dump_script(self, create=True):
        def get_all_same(arr):
            if not arr: return (False, None)
            import operator
            val = arr[0]
            return (len(arr) == operator.countOf(arr,val), val)
        print "hsfem = hs.HSFemale.create_female(%s, attach=True)"%(repr(self.name))
        print "hsfem.reset()"
        anmData = self.stChara.anmMng.anmData
        if anmData and anmData.abdataPath and anmData.filePath:
            print 'hsfem.load_animation(%s, %s)'%(repr(anmData.abdataPath), repr(anmData.filePath))
        if self.stChara.ikCtrl.ikEnable:
            ik = self.studio.studioUIIK       
            if ik.fileNameIF.text: 
                print 'hsfem.play_ik(%s)'%(repr(ik.fileNameIF.text))
        print "hsfem.move(pos=%s, rot=%s)"%(str(self.pos), str(self.rot))        
        # print "hsfem.chara.SetActiveTop(%s)"%(self.chara.GetActiveTop())
        print "hsfem.chara.ChangeBlinkFlag(%s)"%(self.chara.GetBlinkFlag())
        print "hsfem.chara.ChangeEyesPtn(%s,True)"%(self.chara.GetEyesPtn())
        print "hsfem.chara.ChangeMouthPtn(%s,True)"%(self.chara.GetMouthPtn())
        print "hsfem.chara.ChangeLookNeckPtn(%s)"%(self.chara.GetLookNeckPtn())
        print "hsfem.chara.ChangeLookEyesPtn(%s)"%(self.chara.GetLookEyesPtn())
        
        hand_positions = get_hand_positions()
        lposname = hand_positions[self.stChara.anmMng.hand_L_Type]
        rposname = hand_positions[self.stChara.anmMng.hand_R_Type]
        print("hsfem.set_hand_position('l', %s)"%repr(lposname))
        print("hsfem.set_hand_position('r', %s)"%repr(rposname))
        
        clothes = self.chara.statusInfo.clothesState
        (ok, state) = get_all_same(clothes)
        if ok: 
            print "hsfem.set_clothes_state_all(%d)"%state
        else:
            print "hsfem.set_clothes_state(%s)"%str([x for x in clothes])
            
        accessories = self.chara.statusInfo.showAccessory
        (ok, state) = get_all_same(accessories)
        if ok: 
            print "hsfem.enable_accessories(%d)"%state
        else:
            print "hsfem.enable_accessories(%s)"%str([x for x in accessories])
        

class HSItem(HSObject):
    def __init__(self, name=None, stChara=None):
        HSObject.__init__(self, None)
        self.type = 'item'
        self.name = name
        if stChara:
            self.chara = stChara
            self.stChara = stChara
            if not name: self.name = translate(stChara.itemData.name)
        pass

        
    def attach(self, name=None):
        if self.stChara != None:
            return self
        name = self.name.lower()
        for kvp in self.studio.ItemList:
            stItem = kvp.Value
            if stItem.objCtrl:
                if not name or name == translate(stItem.itemData.name).lower():
                    self.stChara = stItem
                    self.chara = self.stChara
                    break
        return self

    @classmethod
    def attach_item(cls, name=None):
        from Manager import Studio
        studio = Studio.Instance
        name = name.lower() if name else None
        for kvp in studio.ItemList:
            stItem = kvp.Value
            if stItem.objCtrl:
                if not name or name == translate(stItem.itemData.name).lower():
                    return cls(name=stItem.itemData.name, stChara=stItem)
        return None
        
    def create(self):
        import StudioItem
        from System import UInt32
        studio = self.studio
        itemList = studio.studioIM.loader.itemList
        id = None
        name = self.name.lower()
        for kvp in itemList:
            stItem = kvp.Value
            if translate(stItem.name).lower() == name:
                #id = stItem
                id = kvp.Key
                break
        if id != None: 
            @unity
            def run(name, id, uid):
                # from UnityEngine import Vector3, Quaternion
                # pos, rot = Vector3.zero, Quaternion.identity
                #return StudioItem(name, id.packPath, id.filePath, id.manifest, pos, rot, uid, id.group)
                from Manager import Studio
                studio = Studio.Instance
                return studio.AddItem(id)
                
            self.stChara = run(self.name, id, studio.unitID)
            self.chara = self.stChara
        return self
        
    @staticmethod
    def create_item(name, attach=False):
        if attach:
            item = HSItem.attach_item(name)
            if item: return item
        return HSItem(name).create()
        
    def __repr__(self):
        return "HSItem(%s)"%repr(self.name)
        
    def dump_script(self, create=True):
        print "item = hs.HSItem.create_item(%s, attach=True)"%(repr(self.name))
        print "item.move(pos=%s, rot=%s)"%(str(self.pos), str(self.rot))
        
def dump_scene(create=True):
    from Manager import Studio
    studio = Studio.Instance
    print "import hs"
    print "hs.reset(); hs.configsetup()"
    HSCamera.dump()
    if studio.FemaleList:
        print '# begin females'
        for kvp in studio.FemaleList:
            sc = kvp.Value
            if sc.body and sc.female:
                hsfem = HSFemale(chara=sc.female)
                hsfem.dump_script(create=create)
                
    if studio.ItemList:
        print '# begin items'
        for kvp in studio.ItemList:
            stItem = kvp.Value
            if stItem.objCtrl:
                hsitem = HSItem(stChara=stItem)
                hsitem.dump_script(create=create)
