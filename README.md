# Apprentice-Bot
Multipurpose Discord bot fo apprentices of Jesus Christ

## List of commands
1. $register [Username - opt] [BDay] register a user in bot's users database

## XML Database structure
* root
    * Users
        * User1 [Name : str, BDay : Date]
        * ...
        * UserN
    * Channels
        * Channel1 [Id : str]
            * User1 [Name : str]
            * ...
            * UserN
        * ...
        * ChannelN