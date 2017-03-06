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

@unity
def capture():
    from HS.Utility import ScreenShot
    ScreenShot.PerformCapture()
    
@unity
def quit():
    from Manager import Scene
    scene = Scene.Instance
    scene.GameEnd(False)

@unity
def move_camera(pos=None, dir=None, angle=None):
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

@unity
def place_char(type, file):
    from Manager import Studio
    from os import path
    charpath = get_char_dir(type)
    if charpath:
        charfile = path.join(charpath, file)
        if path.exists(charfile):
            if type == 'female':
                Studio.Instance.AddFemale(charfile)
            elif type == 'male':
                Studio.Instance.AddMale(charfile)

                
def get_anime_folderlist():
    from UnityEngine import Object
    import H_AnimeFolderListScrollController
    a = Object.FindObjectsOfTypeAll(H_AnimeFolderListScrollController)
    return None if len(a) == 0 else a[0]
    
    
def translate(value):
    import UnityEngine.UI.Translation
    return UnityEngine.UI.Translation.TextTranslator.Translate(value)
    
    