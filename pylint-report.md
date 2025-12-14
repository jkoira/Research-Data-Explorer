# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta:

```
************* Module app
app.py:107:0: C0301: Line too long (120/100) (line-too-long)
app.py:110:0: C0301: Line too long (118/100) (line-too-long)
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:31:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:47:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:78:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:135:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:146:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:155:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:208:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:228:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:228:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:251:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:271:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:325:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:339:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:325:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:348:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:390:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:399:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:390:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:410:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:418:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:24:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:24:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module items
items.py:1:0: C0114: Missing module docstring (missing-module-docstring)
items.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:30:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:36:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:53:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:67:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:83:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:89:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:95:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:136:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:169:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:175:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:189:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:202:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:12:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:33:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
users.py:39:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.59/10 (previous run: 8.56/10, +0.03)

```

Käydään seuraavaksi läpi tarkemmin raportin sisältö ja perustellaan, miksi kyseisiä asioita ei ole korjattu sovelluksessa.

## Liian pitkät rivit
app.py:107:0: C0301: Line too long (120/100) (line-too-long)
app.py:110:0: C0301: Line too long (118/100) (line-too-long)

Ilmoitukset koskevat kahta samantyyppistä return komentoa:

```return redirect(f"/find_dataset?query={query}&data_type={data_type}&scientific_field={scientific_field}&page=1")```

Rivi on tyylinmukaisesti hieman liian pitkä, mutta koska se on yhtenäinen lauseke, sitä on vaikea lyhentää rivinvaihdolla. Tästä syystä sovelluksen kehittäjä on jättänyt sen korjaamatta.



## Docstring-ilmoitukset

Suuri osa raportin ilmoituksista on seuraavan tyyppisiä ilmoituksia:

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Nämä ilmoitukset tarkoittavat, että moduuleissa ja funktioissa ei ole docstring-kommentteja. Sovelluksen kehityksessä on tehty tietoisesti päätös, ettei käytetä docstring-kommentteja.

## Tarpeeton else

Raportissa on seuraavat ilmoitukset liittyen `else`-haaroihin:

```
app.py:339:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:399:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
users.py:33:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
```

Esimerkiksi ensimmäinen ilmoitus koskee seuraavaa koodia:

```python
if "remove" in request.form:
    items.remove_item(item_id)
    return redirect("/")
else:
    return redirect("/item/" + str(item_id))
```

Tämä koodi olisi mahdollista kirjoittaa seuraavasti tiiviimmin:

```python
if "remove" in request.form:
    items.remove_item(item_id)
    return redirect("/")
return redirect("/item/" + str(item_id))
```

Kuitenkin sovelluksen kehittäjän näkemyksen mukaan tällaisissa tapauksissa on selkeämpää kirjoittaa `else`-haara, koska se tuo esille kaksi vaihtoehtoa, miten koodi voi toimia eri tilanteissa. Näin on toimittu myös kurssiesimerkissä.

## Puuttuva palautusarvo

Raportissa on seuraavat ilmoitukset liittyen funktion palautusarvoon:

```
app.py:228:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:325:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:390:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
```

Nämä ilmoitukset liittyvät tilanteeseen, jossa funktio käsittelee metodit `GET` ja `POST` mutta ei muita metodeja. Esimerkiksi ensimmäinen ilmoitus koskee seuraavaa funktiota.

Näissä funktio palauttaa arvon, kun `request.method` on `GET` tai `POST`, mutta periaatteessa voisi tulla tilanne, jossa `request.method` on jotain muuta eikä koodi palauttaisi arvoa. Käytännössä tällainen tilanne ei ole kuitenkaan mahdollinen, koska funktion dekoraattorissa on vaatimus, että metodin tulee olla `GET` tai `POST`. Niinpä tässä tapauksessa ei ole riskiä, että funktio ei jossain tilanteessa palauttaisi arvoa.

## Vakion nimi

Raportissa on seuraava ilmoitus liittyen vakion nimeen:

```
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
```

Tässä koodin päätasolla määritelty muuttuja tulkitaan vakioksi, jonka nimen tulisi olla kirjoitettu suurilla kirjaimilla. Kuitenkin sovelluksen kehittäjän näkemyksen mukaan tässä tilanteessa näyttää paremmalta, että muuttujan nimi on pienillä kirjaimilla. Muuttujaa käytetään koodissa näin:

```python
app.secret_key = config.secret_key
```
Näin on toimittu myös kurssiesimerkissä.

## Vaarallinen oletusarvo

Raportissa on seuraavat ilmoitukset liittyen vaaralliseen oletusarvoon:

```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```

Esimerkiksi ensimmäinen ilmoitus koskee seuraavaa funktiota:

```python
def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()
```

Tässä parametrin oletusarvo `[]` on tyhjä lista. Tässä ongelmaksi voisi tulla, että sama oletusarvona oleva tyhjä listaolio on jaettu kaikkien funktion kutsujen kesken ja jos jossain kutsussa listan sisältöä muutettaisiin, tämä muutos näkyisi myös muihin kutsuihin. Käytännössä tässä tapauksessa tämä ei kuitenkaan haittaa, koska koodi ei muuta listaoliota. Näin on myös kurssiesimerkissä.