# Fuvar Adminisztráció

A Fuvar Adminisztráció egy asztali alkalmazás, amely segít a fuvarok, sofőrök és járművek nyilvántartásában és kezelésében. Az alkalmazás lehetővé teszi a munkaórák, szállítási adatok és szabadságok nyomon követését, valamint különböző témák és egyedi beállítások alkalmazását.

## Funkciók

- Sofőrök, járművek és címek nyilvántartása
- Munkaórák és szállítási adatok kezelése
- Szabadságok nyilvántartása
- Különböző témák (világos, sötét, egyedi) alkalmazása
- Egyedi színek és betűtípusok beállítása
- Teljes képernyős mód támogatása

## Telepítés

1. Klónozd a repozitóriumot a GitHub-ról:

    
    git clone https://github.com/szaat80/fuvarok_projekt.git
    cd fuvarok_projekt
    

2. Hozz létre egy virtuális környezetet és aktiváld azt:

    
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    

3. Telepítsd a szükséges csomagokat:

    
    pip install -r requirements.txt
    

4. Futtasd az alkalmazást:

    
    python run.py
    

## Használat

1. Indítsd el az alkalmazást a fenti parancs segítségével.
2. Jelentkezz be a felhasználónév és jelszó megadásával.
3. Használd a menüket és a gombokat a sofőrök, járművek és címek nyilvántartásához és kezeléséhez.
4. Válaszd ki a kívánt témát és egyedi beállításokat a 
Beállítások menüben.

## Beállítások

A Beállítások menüben lehetőséged van különböző témák (világos, sötét, egyedi) kiválasztására, valamint egyedi színek és betűtípusok beállítására.

### Téma kiválasztása

- **Világos téma:** Alapértelmezett világos téma fekete betűszínnel.
- **Sötét téma:** Sötét téma fehér betűszínnel.
- **Egyedi téma:** Egyedi színek és betűtípusok beállítása.

### Szín és betűtípus beállítása

- **Alapszín:** Válassz egy színt a színválasztó segítségével.
- **Betűtípus:** Válassz egy betűtípust a betűtípus választó segítségével.

## Hozzájárulás

Ha szeretnél hozzájárulni a projekthez, kérlek kövesd az alábbi lépéseket:

1. Forkold a repozitóriumot.
2. Hozz létre egy új ágat a fejlesztéshez:

    
    git checkout -b feature/uj-funkcio
    

3. Végezze el a módosításokat és commitold azokat:

    
    git commit -m Hozzáadva
egy
új
funkció
    

4. Pushold az ágat a GitHub-ra:

    
    git push origin feature/uj-funkcio
    

5. Nyiss egy Pull Request-et a módosítások beolvasztásához.

## Licenc

Ez a projekt az MIT licenc alatt áll. További részletekért lásd a [LICENSE](LICENSE) fájlt.

## Kapcsolat

Ha bármilyen kérdésed vagy észrevételed van, kérlek lépj kapcsolatba velem a [GitHub profilomon](https://github.com/szaat80).
