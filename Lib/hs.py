#import UnityEngine

def call(func, args=(), **kwargs):
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

def capture():
    import screenshot
    screenshot.capture()
    
@unity
def quit():
    from Manager import Scene
    scene = Scene.Instance
    scene.GameEnd(False)

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
    import hs
    from os.path import abspath, join
    cdir = hs.get_char_dir(chartype)
    return [(get_char_name(abspath(join(cdir, fname)), chartype), fname) for fname in hs.list_char(chartype)]
    
@unity
def place_char(type, file):
    from Manager import Studio
    from os import path
    charpath = get_char_dir(type)
    if charpath:
        charfile = path.join(charpath, file)
        if path.exists(charfile):
            if type == 'female':
                return Studio.Instance.AddFemale(charfile)
            elif type == 'male':
                return Studio.Instance.AddMale(charfile)
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
    import StudioFemale, StudioMale, StudioChara, CharMale, CharFemale
    from Manager import Studio
    studio = Studio.Instance
    if isinstance(chara, (CharFemale,CharMale)):
        id, schar = get_studio_char_from_char(chara)
        if id == None: return None
        chara = schar
    if isinstance(chara, (StudioFemale, StudioMale)):
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

#TODO: how to get list of animations with english name?        
_personaList = 'Custom Cheerful Tsundere Gentle Withdrawn Yandere Easygoing Strict Boyish Energetic Diligent Sitri Dance'.split(' ')
_personaMap = dict((y.lower(),x) for x,y in enumerate(_personaList))

@unity
def load_personality(chara, personality):
    import Manager
    if not isinstance(personality, int):
        personality = _personaMap.get(str(personality).lower(), None)
    if personality == None: return
    stChara = focus_studio_char(chara)
    adv = Manager.ADV.Instance
    ok, ai = adv.animeInfo.TryGetValue(personality)
    if ok and ai:
        chara.LoadAnimation(ai.assetbundle, ai.file)
        class AnimationPlayer(object):
            def __init__(self, owner, personality, names, map):
                self._owner = owner
                self.names = names
                self._map = map
                self.personality = _personaList[personality]
                
            def play(self, animation):
                if isinstance(animation, int):
                    animation = self.names[animation]
                data = self._map.get(str(animation).lower(), None)
                if data:
                    self._owner.ChangeAnime(data,0)
                
        # now that personality is loaded.  Addition animations are available in base list
        animeDict = Manager.Studio.Instance.charaListScrollController.animeListScrlCtrl.stAnimeDataList
        animeNames = [kvp.Value.clipName for kvp in animeDict]
        animeMap = dict( ( (kvp.Value.clipName.lower(), kvp.Value) for kvp in animeDict ) )
        return AnimationPlayer(stChara, personality, animeNames, animeMap)
    return None


def translate(value):
    import UnityEngine.UI.Translation
    return UnityEngine.UI.Translation.TextTranslator.Translate(value)
    
    