from hs import unity, call


#Setup configuration to be favorable for screenshots
@unity
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

@unity
def load_hanime(hlisttype, hlist, anim):
    """Load specific animation by number"""
    from Manager import Studio
    import UnityEngine
    import hs
    import types
    studio = Studio.Instance
    hAnime = studio.hAnimeListScrlCtrl
    hFolder = hs.get_anime_folderlist()
    try:
        htypelist = ['Fondle','Service','Insert','Other']
        if isinstance(hlisttype, str):
            try:
                hlisttype = htypelist.index(hlisttype)
            except:
                print "Animation Type (%s) not found.  Must be one of:"%(hlisttype)
                print " ".join(htypelist)
                return                
        if hlisttype < 0 or hlisttype >= len(hFolder.hTypeToggles):
            return
       
        nowHType = studio.nowHType
        nowHStyleIndex = studio.nowHStyleIndex
        info = studio.lstAnimInfo[nowHType][nowHStyleIndex]
        animlist = [x.clipName for x in studio.hClipNameList[info.clipType].Values]
        if isinstance(anim, str):
            try:
                anim = animlist.index(anim)
            except:
                print "Animation not found.  Must be one of:"
                print " ".join(animlist)
                return
            
        if anim < 0 or anim >= len(animlist):
            return
            
        hFolder.hTypeToggles[hlisttype].isOn = True
        hFolder.ChangeHTypeToggle(hlisttype)
        hFolder.ChangeAnimeFolder(hlist, False)
        hAnime.ChangeAnime(anim)
        hAnime.MaleMoveToFemalePos()
        
        
    except Exception as ex:
        print(ex)
        pass

def run():
    from Manager import Studio
    import hs
    import time
    
    # reset the studio to blank
    hs.reset()
    
    # set the camera settings to be favorable to transparent screenshots
    setupconfig()
    
    studio = Studio.Instance
    hAnime = studio.hAnimeListScrlCtrl

    # load sample girl and make default on h animation
    @unity
    def createfemale(file):
        studio.SelectSex = 1
        hs.place_char('female', file)
        hAnime.CurrentCharaSet()
    createfemale('sample_female.png')
    
    # load sample male and make default on h animation
    @unity
    def createmale(file):
        studio.SelectSex = 0
        hs.place_char('male', file)
        hAnime.CurrentCharaSet()
    createmale('sample_male.png')
    
    # load an animation and move the camera
    load_hanime(0,0,0)
    hs.move_camera(pos = (0,0.8,0), dir = (0.0,0.0,-5.0), angle=(43.7,223.4,0.0))
    
    time.sleep(2)
    hs.capture()
    
    load_hanime('Service',1,'SLoop')
    time.sleep(2)
    hs.capture()
    
    
    