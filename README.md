# DSA - Distribuovaná kritická sekce

## Zadání

Vytvořit distribuovaný algoritmus který realizuje kritickou sekci pomocí apache zookeeper

## Editace docker file

Jediné změny které se týkají dockerfilu jsou nahrání scriptu a editace pravomocí na spustitelný shell script

## Implementace algoritmu

Jako mé předchozí řešení aplikace jde spustit pomocí vagrant file. Nejprve při spuštění klient naváže spojení s ZOONODE clientem pomocí zk.start(). Následně vytvoří pomocí Lock(zk, '/distributed_lock') zámek který bude sloužit jako vlajka pro přístup do kritické sekce. Všechny procesy se následně snaží v zadaném intervalu dostat do kritické sekce a zapsat. Jediná úprava oproti zadaní je přidání intervalu pro uzel který úspěšně zapíše do kritické sekce. Důvodem byla velmi malá pradvěpodobnost že se ostatní procesy do sekce dostanou.

## Chyby

Bohužel jediné co jsem dvě věci které jsem nevyřešil je ztráta zámku když proces spadne při odesílání dat. Dalším problémem který jsem nevyřešil jsou ostantí clienti. Mým jediným tipem na to co by problém mohl být je limitace připojení na jednoho hosta.

## Závěr

Tato distribuovaná aplikace funguje funguje dostatečně díky dalšímu zpoždění po zápisu. Respektive demonstruje že se procesy střídají v zapisovaní do krititické sekce.
---
