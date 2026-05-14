import bpy
import math
import os

SCIEZKA_LAB07 = r"C:/Users/Admin/Desktop/kwiatek.blend"
NAZWA_KOLEKCJI = "Roslina_Hero"
PREFIX_LISCIA = "Roslina_Lisc"
KLATKA_KONIEC_GLOBALNA = 240 


def wyczysc_animacje(obj):
    if obj.animation_data and obj.animation_data.action:
        bpy.data.actions.remove(obj.animation_data.action)

def animuj_lisc(obj, faza, czestosc=0.05, amplituda=0.3, klatka_start=1, klatka_koniec=240):
    wyczysc_animacje(obj)
    rotacja_bazowa_y = obj.rotation_euler[1]
    
    for klatka in range(klatka_start, klatka_koniec + 1):
        kat = rotacja_bazowa_y + amplituda * math.sin(klatka * czestosc + faza)
        obj.rotation_euler[1] = kat
        obj.keyframe_insert(data_path="rotation_euler", frame=klatka, index=1)

def animuj_wszystkie_liscie(prefix_nazwy):
    liscie = [obj for obj in bpy.data.objects if obj.name.startswith(prefix_nazwy)]

    for i, lisc in enumerate(liscie):
        faza_lisc = i * (2 * math.pi / max(len(liscie), 1))
        animuj_lisc(lisc, faza=faza_lisc, klatka_koniec=KLATKA_KONIEC_GLOBALNA)
    

def importuj_rosline(sciezka_blend, nazwa_kolekcji):
    if not os.path.exists(sciezka_blend):
        return False

    sciezka_kolekcji = os.path.join(sciezka_blend, "Collection", nazwa_kolekcji)
    
    try:
        bpy.ops.wm.append(
            filepath=sciezka_kolekcji,
            directory=os.path.join(sciezka_blend, "Collection"),
            filename=nazwa_kolekcji,
        )
        return True
    except Exception as e:
        return False

def animuj_pak(nazwa_obj="Pąk", klatka_start=20, klatka_koniec=240,
               skala_min=0.0, skala_max=0.3):
    obj = bpy.data.objects.get(nazwa_obj)
   
    wyczysc_animacje(obj)

    obj.scale = (skala_min, skala_min, skala_min)
    obj.keyframe_insert(data_path="scale", frame=1)

    obj.keyframe_insert(data_path="scale", frame=klatka_start)

    obj.scale = (skala_max, skala_max, skala_max)
    obj.keyframe_insert(data_path="scale", frame=klatka_koniec)

if __name__ == "__main__":
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = KLATKA_KONIEC_GLOBALNA

    sukces = importuj_rosline(SCIEZKA_LAB07, NAZWA_KOLEKCJI)
    
    if sukces:
        animuj_wszystkie_liscie(PREFIX_LISCIA)
        
        animuj_pak(nazwa_obj="Pąk", klatka_start=20, klatka_koniec=KLATKA_KONIEC_GLOBALNA)
        
        bpy.context.scene.frame_set(1)