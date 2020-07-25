# GameSystem
A Discord Bot for playing Tabletop Role-Playing-Games using Raymag's system.

Want to add this bot? [Click here!](https://discord.com/api/oauth2/authorize?client_id=735522883597500487&scope=bot&permissions=1)

## Commands
1. [$roll <dice> [opt:modifier]](#roll)
2. [$newchar <name>](#newchar)
3. [$chars](#chars)
4. [$char <index>](#char)
5. [$setmain <index>](#setmain)
6. [$delchar <index>](#delchar)
7. [$test <type>](#test)
8. [$hit <username> <damage>](#hit)
9. [$rest](#rest)


## $roll

The roll command allows you to roll different type of dice, be it a d20, d6 or d8. You can use it with the following sintaxe.
```
$roll <dice> [opt:modifier]
```
Examples:
```
$roll d20 + 10
$roll 3d6
$roll d8 - 2
```

## $newchar 

This command allows a player to generate its own character with a straight and simple sintaxe. You can choose a name and a standard character sheet will be generated and stored online.

```
$newchar <name>
```

 The character will also receive a **random magic affinity** that can be currently one of the *4 basic natural elements* (fire, water, earth and air). Each element gives your character different attributes.

Examples:
```
$newchar Thorin
$newchar Lamasc casca aguda
```

## $chars

This simple command allows a player to see all his characters sheets in a ordered way. $chars also shows the player which character is the current main character. 

Example:
```
$chars
```

## $char

If $chars shows you all your characters, $char is the perfect command to get all the info about a specific character you own. You just need to call the command and pass the **index** of the character, which can be get with the command $chars.

```
$char <index>
```

Examples:
```
$char 1
$char 3
$char 7
```

## $setmain

With $setmain you are able to easily set your main character sheet among a bunch of them. You just need to call the command and pass the **index** or **position** of the character you want to set as the *main*.

```
$setmain <index>
```

Examples:
```
$setmain 1
$setmain 7
$setmain 9
```

## $delchar 

This command allows a player to delete one of its characters with a single sentence. You just need to pass  the **index / position** of the characters and the magic will be done.

```
$delchar <index>
```

Example:
```
$delchar 4
$delchar 6
$delchar 2
```

## $test

With $test command, a player can easily execute tests of attributes in a really practical and fast way. All it's necessary to do is type the command and pass the attribute of the test.

Sintax:
```
$test <type>
```

Example:
```
$test str
$test dex
$test int
```

## $hit

This command allows you to hurt a character, and maybe even kill it. All it's necessary to do is call the command and pass the username of the player, plus the damage to be done.

Sintax:
```
$hit <username> <damage>
```

Example:
```
$hit Luciano 4
$hit Valkyria 8
```

## $rest

With $rest command a player can easily recover all damage and stress of a character in just one sentence.

Sintax & Example:
```
$rest
```
