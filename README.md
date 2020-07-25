# GameSystem
A Discord Bot for playing Tabletop Role-Playing-Games using Raymag's system.

Want to add this bot? [Click here!](https://discord.com/api/oauth2/authorize?client_id=735522883597500487&scope=bot&permissions=1476619362)

## Commands
1. [$roll](#roll)
2. [$newchar](#newchar)
3. [$chars](#chars)
4. [$char](#char)
5. [$setmain](#setmain)
6. [$delchar](#delchar)
7. [$test](#test)
8. [$hit](#hit)
9. [$rest](#rest)
10. [$res](#res)
11. [$givexp](#givexp)
12. [$givegold](#givegold)
13. [$iattr](#iattr)

<p align=center>
<img width=60% src=https://media.giphy.com/media/duexIlfr9yYwYE23UA/giphy.gif>
</p>


## $roll

The roll command allows you to roll different type of dice, be it a d20, d6 or d8. You can use it with the following sintaxe.
```bash
$roll <dice> [opt:modifier]
```
Examples:
```bash
$roll d20 + 10
$roll 3d6
$roll d8 - 2
```

## $newchar 

This command allows a player to generate its own character with a straight and simple sintaxe. You can choose a name and a standard character sheet will be generated and stored online.

```bash
$newchar <name>
```

 The character will also receive a **random magic affinity** that can be currently one of the *4 basic natural elements* (fire, water, earth and air). Each element gives your character different attributes.

Examples:
```bash
$newchar Thorin
$newchar Lamasc casca aguda
```

## $chars

This simple command allows a player to see all his characters sheets in a ordered way. $chars also shows the player which character is the current main character. 

Example:
```bash
$chars
```

## $char

If $chars shows you all your characters, $char is the perfect command to get all the info about a specific character you own. You just need to call the command and pass the **index** of the character, which can be get with the command $chars.

```bash
$char <index>
```

Examples:
```bash
$char 1
$char 3
$char 7
```

## $setmain

With $setmain you are able to easily set your main character sheet among a bunch of them. You just need to call the command and pass the **index** or **position** of the character you want to set as the *main*.

```bash
$setmain <index>
```

Examples:
```bash
$setmain 1
$setmain 7
$setmain 9
```

## $delchar 

This command allows a player to delete one of its characters with a single sentence. You just need to pass  the **index / position** of the characters and the magic will be done.

```bash
$delchar <index>
```

Example:
```bash
$delchar 4
$delchar 6
$delchar 2
```

## $test

With $test command, a player can easily execute tests of attributes in a really practical and fast way. All it's necessary to do is type the command and pass the attribute of the test.

Sintax:
```bash
$test <type>
```

Example:
```bash
$test str
$test dex
$test int
```

## $hit

This command allows you to hurt a character, and maybe even kill it. All it's necessary to do is call the command and pass the username of the player, plus the damage to be done.

Sintax:
```bash
$hit <username> <damage>
```

Example:
```bash
$hit Luciano 4
$hit Valkyria 8
```

## $rest

With $rest command a player can easily recover all damage and stress of a character in just one sentence.

*A dead character cannot rest. It already rests in peace.*

Sintax & Example:
```bash
$rest
```

## $res

With **$res** a **Game Master** can easily ressurect any main character. Just call the command followed by the owner's username of the character you want to ressurect.

Sintax:
```bash
$res <username>
```

Example:
```bash
$res Raymag
```

## $givexp

This command allows **Game Masters** to give XP to any main character in the game. Just type the command and pass the ammount of XP followed by all the owner's username of the characters you want to give points to.

*By getting more XP, a character can level up. By leveling up, a character can get IP and CP which can be later used to rise the attributes stats and acquire skills.*

Syntax:
```bash
$givexp <xp> [username]
```

Example:
```bash
$givexp 10 Raymag INefasto Excallibur
```

## $givegold

This command allows **Game Masters** to give gold to a list of characters. All you need to do is call the command, passing the ammount of gold and the username of all the players you want to give gold to.

Syntax:
```bash
$givegold <gold> [username]
```

Example:
```bash
$givegold Raymag Jaina Lux
```

## $iattr

With this command, a player can increase his attributes stats in exchange of **CP (character points)**. A character can get CP by raising its level.

Syntax:
```bash
$iattr <attr>
```

Example:
```bash
$iattr dex
```