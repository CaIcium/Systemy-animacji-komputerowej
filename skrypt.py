import bpy
import random
import math

# słownik roslin 
TYPY_ROSLIN = {
    "drzewo": {
        "wysokosc": (4.0, 7.0),
        "liczba_lisci": (3, 5),     
        "promien_lisci": (1.2, 1.8),
        "liczba_korzeni": (4, 6),
        "kolor_lodygi": (0.15, 0.08, 0.02, 1),
        "kolor_lisci": (0.02, 0.18, 0.06, 1),
    },
    "krzew": {
        "wysokosc": (0.8, 2),
        "liczba_lisci": (3, 4),
        "promien_lisci": (0.6, 1.2),
        "liczba_korzeni": (2, 4),
        "kolor_lodygi": (0.25, 0.15, 0.05, 1),
        "kolor_lisci": (0.1, 0.5, 0.05, 1),
    },
    "paproc": { 
        "wysokosc": (1.4, 2.2),        
        "liczba_lisci": (30, 40),     
        "promien_lisci": (0.08, 0.12), 
        "liczba_korzeni": (2, 4),
        "kolor_lodygi": (0.1, 0.4, 0.1, 1), 
        "kolor_lisci": (0.15, 0.55, 0.2, 1),
    },
}

def stworz_rosline(pozycja, wysokosc, liczba_lisci, promien_lisci, liczba_korzeni, typ):
    """Generuje kompletny model rośliny i zwraca listę jej elementów."""
    obiekty = []
    x, y, z = pozycja 
    
    # 1. Tworzenie pnia/rdzenia roslin
    if typ == "paproc":
        rdzen_wysokosc = 0.1
        rdzen_promien = 0.1
    else:
        rdzen_wysokosc = wysokosc
        rdzen_promien = 0.15
        
    bpy.ops.mesh.primitive_cylinder_add(
        radius=rdzen_promien, 
        depth=rdzen_wysokosc, 
        location=(x, y, z + rdzen_wysokosc / 2)
    )
    lodyga = bpy.context.active_object
    obiekty.append(lodyga)
    
    # Tworzenie liści w zależności od typu pnia mamy dzewio krzew i paroć 
    if typ == "drzewo":
   
        for i in range(liczba_lisci):
            obecny_promien = promien_lisci * (1.0 - (i / liczba_lisci) * 0.6)
            wysokosc_stozka = wysokosc * 0.4
            z_stozka = z + (wysokosc * 0.3) + (i * wysokosc_stozka * 0.5) + (wysokosc_stozka / 2)
            
            bpy.ops.mesh.primitive_cone_add(
                radius1=obecny_promien,
                depth=wysokosc_stozka,
                location=(x, y, z_stozka)
            )
            igly = bpy.context.active_object
            obiekty.append(igly)
 
    if typ == "paproc":
        promien_kuli_bazy = 0.25 

        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=12, ring_count=8, 
            radius=promien_kuli_bazy, 
            location=(x, y, z) 
        )
        kula_baza = bpy.context.active_object
        obiekty.append(kula_baza)

        # Generowanie kolców ( liscie paproci)
        for _ in range(liczba_lisci):
            phi = random.uniform(0, 2 * math.pi)
            costheta = random.uniform(-1, 1) 
            sintheta = math.sqrt(1 - costheta * costheta)

            vx = sintheta * math.cos(phi)
            vy = sintheta * math.sin(phi)
            vz = costheta

            #miejsce w ktorym maja byc kolce 
            embedded_depth = wysokosc * 0.05 
            offset = promien_kuli_bazy + wysokosc / 2 - embedded_depth
            
            kx = x + vx * offset
            ky = y + vy * offset
            kz = z + vz * offset

            ry = math.atan2(math.sqrt(vx**2 + vy**2), vz)
            rz = math.atan2(vy, vx)

            bpy.ops.mesh.primitive_cone_add(
                vertices=8, 
                radius1=promien_lisci,
                depth=wysokosc,
                location=(kx, ky, kz),
                rotation=(0, ry, rz)
            )
            kolec = bpy.context.active_object
            obiekty.append(kolec)
    if typ == "krzew":
        z_szczyt = z + wysokosc
        for _ in range(liczba_lisci):
            offset_x = random.uniform(-promien_lisci/2, promien_lisci/2)
            offset_y = random.uniform(-promien_lisci/2, promien_lisci/2)
            offset_z = random.uniform(-promien_lisci/2, promien_lisci/2)
            
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=promien_lisci, 
                location=(x + offset_x, y + offset_y, z_szczyt + offset_z)
            )
            lisc = bpy.context.active_object
            obiekty.append(lisc)
            
    return obiekty

def stworz_material(nazwa, kolor_rgba):
    mat = bpy.data.materials.get(nazwa)
    if not mat:
        mat = bpy.data.materials.new(name=nazwa)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = kolor_rgba
    return mat

def stworzroslinetyp(x, z, typ):
    parametry = TYPY_ROSLIN[typ]
    
    wysokosc = random.uniform(*parametry["wysokosc"])
    liczba_lisci = random.randint(*parametry["liczba_lisci"])
    promien_lisci = random.uniform(*parametry["promien_lisci"])
    liczba_korzeni = random.randint(*parametry["liczba_korzeni"])
    
    obiekty_rosliny = stworz_rosline((x, z, 0), wysokosc, liczba_lisci, promien_lisci, liczba_korzeni, typ)
    
    mat_lodygi = stworz_material(f"Mat_Lodyga_{typ}", parametry["kolor_lodygi"])
    mat_lisci = stworz_material(f"Mat_Liscie_{typ}", parametry["kolor_lisci"])
    
    if obiekty_rosliny:
        obiekty_rosliny[0].data.materials.append(mat_lodygi)
        for lisc in obiekty_rosliny[1:]:
            if hasattr(lisc.data, "materials"):
                lisc.data.materials.append(mat_lisci)
            
    return obiekty_rosliny

def wybierztypbiomu(x, z, rozmiar_pola):
    polowa = rozmiar_pola / 2
    max_odleglosc = max(abs(x), abs(z))
    
    if max_odleglosc < 0.3 * polowa:
        return "drzewo"
    elif max_odleglosc < 0.7 * polowa:
        return "krzew" if random.random() < 0.7 else "drzewo"
    else:
        return "paproc" if random.random() < 0.7 else "krzew"

def generujlas(liczbaroslin=18, rozmiar_pola=10.0, seed=42):
    random.seed(seed)
    
    if "Las" in bpy.data.collections:
        stara_kolekcja = bpy.data.collections["Las"]
        for obj in stara_kolekcja.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(stara_kolekcja)
        
    kolekcja_las = bpy.data.collections.new("Las")
    bpy.context.scene.collection.children.link(kolekcja_las)
    
    # dodanie ziemi
    bpy.ops.mesh.primitive_plane_add(size=rozmiar_pola * 1.5, location=(0, 0, 0))
    ziemia = bpy.context.active_object
    ziemia.name = "Ziemia"
    
    # dzielenie siatki na wiele kwadratow
    subsurf = ziemia.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.subdivision_type = 'SIMPLE'
    subsurf.levels = 5
    
    # wyginianie terenu 
    if "SzumTerenu" not in bpy.data.textures:
        tex = bpy.data.textures.new("SzumTerenu", type='CLOUDS')
        tex.noise_scale = 3.0
    else:
        tex = bpy.data.textures["SzumTerenu"]
        
    displace = ziemia.modifiers.new(name="Displace", type='DISPLACE')
    displace.texture = tex
    displace.strength = 0.4 
    
    for poly in ziemia.data.polygons:
        poly.use_smooth = True

    for coll in ziemia.users_collection:
        coll.objects.unlink(ziemia)
    kolekcja_las.objects.link(ziemia)
    
    mat_ziemia = stworz_material("Mat_Ziemia", (0.03, 0.15, 0.04, 1)) 
    ziemia.data.materials.append(mat_ziemia)
    # -----------------------------------
    
    for _ in range(liczbaroslin):
        x = random.uniform(-rozmiar_pola/2, rozmiar_pola/2)
        z = random.uniform(-rozmiar_pola/2, rozmiar_pola/2)
        
        typ = wybierztypbiomu(x, z, rozmiar_pola)
        utworzone_obiekty = stworzroslinetyp(x, z, typ)
        
        for obj in utworzone_obiekty:
            if obj is not None:
                for coll in obj.users_collection:
                    coll.objects.unlink(obj)
                kolekcja_las.objects.link(obj)

    if "Camera" not in bpy.data.objects:
        bpy.ops.object.camera_add()
    cam = bpy.data.objects["Camera"]
    cam.location = (0, -rozmiar_pola * 1.5, rozmiar_pola) 
    cam.rotation_euler = (math.radians(60), 0, 0)         
    bpy.context.scene.camera = cam
    
    if "Sun" not in bpy.data.objects:
        bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
        sun = bpy.context.active_object
        sun.name = "Sun"
    else:
        sun = bpy.data.objects["Sun"]
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(45), math.radians(30), 0)
    
    scena = bpy.context.scene
    scena.render.resolution_x = 1200
    scena.render.resolution_y = 800
    scena.render.engine = 'BLENDER_EEVEE'
    
    scena.render.filepath = "//las_05.png" 
    
    print("Rozpoczynam renderowanie...")
    bpy.ops.render.render(write_still=True)
    print("Zakończono renderowanie! Plik las_05.png został zapisany.")

if __name__ == "__main__":
    generujlas(liczbaroslin=60, rozmiar_pola=40.0)
