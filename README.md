# AI Agent Timemaster

## Popis projektu
AI agent **Timemaster** je aplikace pro efektivní plánování času a organizaci úkolů. Pomáhá uživateli optimalizovat denní rozvrh, zohledňuje jeho aktuální schůzky a učí se z předchozích zkušeností, aby postupně přesněji odhadoval dobu trvání jednotlivých činností.

Aplikace je postavena na **Tkinter** pro grafické rozhraní a využívá **JSON** pro ukládání trvalých úkolů a naučených dat.

## Funkcionality
- **Analýza rozvrhu:** Aplikace pracuje s pevně definovanými schůzkami a identifikuje volné časové sloty.
- **Dynamické plánování:** Automaticky přiřazuje úkoly do dostupných časových oken.
- **Učení z uživatelských vstupů:** Upravuje odhadovanou dobu trvání úkolů na základě zpětné vazby.
- **Trvalé ukládání úkolů:** Možnost přidat trvalé úkoly, které se opakují.
- **Interaktivní grafické rozhraní:** Umožňuje uživateli jednoduše přidávat úkoly a zobrazovat rozvrh.

## Instalace a spuštění
1. **Požadavky:**
   - Python 3.x
   - Knihovna **tkinter** (součást standardní distribuce Pythonu)

2. **Stažení a spuštění:**
```sh
python AI_agent_Timemaster.py
```

## Struktura projektu
```
AI_agent_Timemaster.py  # Hlavní skript aplikace
|-- timemaster_tasks.json  # Uložené trvalé úkoly
|-- timemaster_learned.json  # Naučené doby trvání úkolů
```

## Použití
1. Spusťte aplikaci.
2. Přidejte nové úkoly do seznamu nebo si nechte vygenerovat plán na základě dostupných časových slotů.
3. Pokud aplikace nabídne zpětnou vazbu, potvrďte skutečný čas strávený úkolem pro vylepšení odhadů do budoucna.

## Budoucí vylepšení
- Integrace s kalendářem (Google Calendar, Outlook).
- Přizpůsobení priorit úkolů.
- Lepší vizualizace denního rozvrhu.

## Autor
**Lukáš Drštička**

**Mindlore AI Solutions**

