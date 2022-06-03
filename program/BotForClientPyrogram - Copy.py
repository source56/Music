from pyrogram import Client, filters, types
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove)
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import ChatAdminRequired

import asyncio


# DAXTA
api_id = 17320595
api_hash ="bb0fbf90e7c8f09160608d1962200221"
bot_token = "5253429858:AAFBLoOUy68KtfFGCXYGXsIkYFNjdvKMsPk"

# CLIENT
app = Client("BotPyrogram", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# OWNER
owner = 5048738026 # owner id or username ( id : as an intger, username : as a string ) ex : id > owner = 5048738026 ----- username > owner = "takeTimw"

# HELP VARS
AddChannel = False
RemoveChannel = False
SendOutToPrivate = False
SendOutToPublic = False

# BOT DATA
AddedChannels = []
users = []
active_users = {}

# BUTTON NAMES
MustJoinShowButtonName = '📑 الاشتراك الاجباري'
StatisticsShowButtonName = '📈 الاحصائيات'
LiveShowButtonName = '📤 الاذاعه'
CheckButtonName = '📑 تأكيد'
AddChannelButtonName = '📑 اضافة قناة'
RemoveChannelButtonName = '📑 حذف قناة'
BackButtonName = 'رجوع'
SendToChannelsButtonName = '📑 الاذاعه في المجموعات'
SendToPrivateButtonName = '📑 الاذاعه في الخاص'


# MAIN KEYBOARD
async def Keyboard(sender):
    if sender.id == owner or sender.username == owner:
        kyeboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(MustJoinShowButtonName, b'click_1')],
                [InlineKeyboardButton(StatisticsShowButtonName, b'click_2')],
                [InlineKeyboardButton(LiveShowButtonName, b'click_3')]
            ]
        )
        await app.send_message(chat_id=sender.id, text='🖥️ This is admin Dashboard.. Only visible for the owner', reply_markup=kyeboard)


# USERS HAS BEEN JOINED ALL CHANNELS
async def NormalUserJoined(sender):
    kyeboard = ReplyKeyboardRemove(selective =True)
    await app.send_message(chat_id=sender.id, text='Welcome here', reply_markup=kyeboard)


# NEW NORMAL USERS CHECKER
async def NormalUser(sender):
    
    kyeboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(CheckButtonName, b'check')]
        ]
    )
    # kyeboard = ReplyKeyboardMarkup([[CheckButtonName]], resize_keyboard=True)
    if len(AddedChannels) == 0:
        RUN = await NormalUserJoined(sender)
    else:
        for channel_id in AddedChannels:
            if sender.id not in active_users:
                active_users[sender.id] = {}
            active_users[sender.id][channel_id] = False
            
            try:
                user = await app.get_chat_member(chat_id=channel_id, user_id=sender.id)
                active_users[sender.id][channel_id] = True
            except:
                active_users[sender.id][channel_id] = False
                MESSAGE = ''
                for channel in AddedChannels:
                    MESSAGE = MESSAGE + '\n'+str(channel)

                await app.send_message(chat_id=sender.id, text=f'You must join all our channels\n\n{MESSAGE}', reply_markup=kyeboard)
                break

        is_member = True
        for channel_id in AddedChannels:
            answer = active_users[sender.id][channel_id]
            if answer == False:
                is_member = False
                break

        if is_member != False:
            RUN = await NormalUserJoined(sender)
            

# MUST JOIN > SHOW ADD & REMOVE BUTTONS
async def ShowAddRemoveButtons(sender):
    
    if sender.id == owner or sender.username == owner:
        kyeboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(AddChannelButtonName, b'Addchannel'), InlineKeyboardButton(RemoveChannelButtonName, b'Removechannel')],
                [InlineKeyboardButton(BackButtonName, b'back')]
            ]
        )
        # kyeboard = ReplyKeyboardMarkup([[AddChannelButtonName, RemoveChannelButtonName], [BackButtonName]], resize_keyboard=True)
        await app.send_message(chat_id=sender.id, text='❕ Choose an action to active it!', reply_markup=kyeboard)

# ADD BUTTON
async def AddButton(sender):
    if sender.id == owner or sender.username == owner:
        await app.send_message(chat_id=sender.id, text='❕ Send channel username ( ex : @zxllkada ):')


# REMOVE BUTTON
async def RemoveButton(sender, chat_id):
    if sender.id == owner or sender.username == owner:
        if len(AddedChannels) == 0:
            kyeboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(BackButtonName, b'back')]
                ]
            )
            order = await app.send_message(chat_id=sender.id, text='❕ No channels!', reply_markup=kyeboard)
        else:
            MESSAGE = ''
            for channel in AddedChannels:
                MESSAGE = MESSAGE + '\n'+str(channel)
            order = await app.send_message(chat_id=sender.id, text=f'{MESSAGE}\n\nSend a username of channel to remove it.')


# STATISTICS
async def Statistics(sender):
    if sender.id == owner or sender.username == owner:
        TotalUsers = len(users)
        TotalJoinedGroups = len(AddedChannels)

        kyeboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(BackButtonName, b'back')]
            ]
        )
        MESSAGE = f'Total users started this bot is {TotalUsers}\n\nTotal Channels using this bot is {TotalJoinedGroups}'
        order = await app.send_message(chat_id=sender.id, text=MESSAGE, reply_markup=kyeboard)


# SEND OUT > SHOW CHANNEL & PRIVATE BUTTONS
async def ShowSendOutButtons(sender):
    if sender.id == owner or sender.username == owner:
        kyeboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(SendToChannelsButtonName, b'SendOutChannel'), InlineKeyboardButton(SendToPrivateButtonName, b'SendOutPrivate')],
                [InlineKeyboardButton(BackButtonName, b'back')]
            ]
        )
        # kyeboard = ReplyKeyboardMarkup([[SendToChannelsButtonName, SendToPrivateButtonName], [BackButtonName]], resize_keyboard=True)
        await app.send_message(chat_id=sender.id, text='❕ Choose something!', reply_markup=kyeboard)
    

# SEND TO CHANNELS BUTTON
async def SendOutToChannelsButton(sender):
    
    if sender.id == owner or sender.username == owner:  
        if len(AddedChannels) == 0:
            kyeboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(BackButtonName, b'back')]
                ]
            )
            await app.send_message(chat_id=sender.id, text='❕ You did not add any channels', reply_markup=kyeboard)
        else:
            await app.send_message(chat_id=sender.id, text='❕ Send anything')


# SEND TO PRIVATE BUTTON
async def SendOutToPrivateButton(sender):
    
    if sender.id == owner or sender.username == owner:
        if len(users) == 0:
            kyeboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(BackButtonName, b'back')]
                ]
            )
            await app.send_message(chat_id=sender.id, text='❕ No users are using this bot', reply_markup=kyeboard)
        else:
            await app.send_message(chat_id=sender.id, text='❕ Send anything')
            


# NEW USER JOINED > START COMMAND
@app.on_message(filters.command("start"))
async def start_command(client, message):
    
    # SHOW MAIN KEYBOARD
    sender = message.from_user
    if sender.id == owner or sender.username == owner:
        if sender.id not in users:
            users.append(sender.id)
        RUN = await Keyboard(message.from_user)
    else:
        if sender.id not in users:
            users.append(sender.id)
        RUN = await NormalUser(message.from_user)



@app.on_callback_query()
async def my_handler(client, message):
    global AddChannel, RemoveChannel, SendOutToPublic, SendOutToPrivate
    
    botMe = await app.get_me()
    
    if message.from_user.id != owner or message.from_user.username != owner:
        # CHECK BUTTON CLICKED
        if message.data == 'check':
            AddChannel = False
            RemoveChannel = False
            SendOutToPublic = False
            SendOutToPrivate = False
            await app.delete_messages(chat_id=message.from_user.id, message_ids=message.message.id)
            RUN = await NormalUser(message.from_user)
            
    if message.from_user.id == owner or message.from_user.username == owner:
        # SHOW ADD & REMOVE BUTTONS
        if message.data == 'click_1':
            AddChannel = False
            RemoveChannel = False
            SendOutToPublic = False
            SendOutToPrivate = False
            await app.delete_messages(chat_id=message.from_user.id, message_ids=message.message.id)
            RUN = await ShowAddRemoveButtons(message.from_user)
                
        # BACK BUTTON CLICKED
        if message.data == 'back':
            AddChannel = False
            RemoveChannel = False
            SendOutToPublic = False
            SendOutToPrivate = False
            await app.delete_messages(chat_id=message.from_user.id, message_ids=message.message.id)
            RUN = await Keyboard(message.from_user)
                   
        # ADD CHANNEL BUTTON CLICKED
        if message.data == 'Addchannel':
            AddChannel = True
            RemoveChannel = False
            SendOutToPublic = False
            SendOutToPrivate = False
        if AddChannel == True:
            await app.delete_messages(chat_id=message.from_user.id, message_ids=message.message.id)
            print (message.message.text)
            RUN = await AddButton(message.from_user)

        # REMOVE CHANNELs BUTTON CLICKED
        if message.data == 'Removechannel':
            RemoveChannel = True
            AddChannel = False
            SendOutToPublic = False
            SendOutToPrivate = False
        if RemoveChannel == True:
            await app.delete_messages(chat_id=message.from_user.id, message_ids=message.message.id)
            RUN = await RemoveButton(message.from_user, message.message.text)
               
        # SHOW STATISTICS
        if message.data == 'click_2':
            RemoveChannel = False
            AddChannel = False
            SendOutToPublic = False
            SendOutToPrivate = False
            await app.delete_messages(chat_id=message.from_user.id, message_ids=message.message.id)
            RUN = await Statistics(message.from_user)
                
        # SHOW SENDOUT BUTTONS
        if message.data == 'click_3':
            RemoveChannel = False
            AddChannel = False
            SendOutToPublic = False
            SendOutToPrivate = False
            await app.delete_messages(chat_id=message.from_user.id, message_ids=message.message.id)
            RUN = await ShowSendOutButtons(message.from_user)
                
        # SENDOUT CHANNELS BUTTON CLICKED
        if message.data == 'SendOutChannel':
            SendOutToPublic = True
            RemoveChannel = False
            AddChannel = False
            SendOutToPrivate = False
        if SendOutToPublic == True:
            await app.delete_messages(chat_id=message.from_user.id, message_ids=message.message.id)
            RUN = await SendOutToChannelsButton(message.from_user)
                
        # SENDOUT PRIVATE BUTTON CLICKED
        if message.data == 'SendOutPrivate':
            SendOutToPrivate = True
            SendOutToPublic = False
            RemoveChannel = False
            AddChannel = False
        if SendOutToPrivate == True:
            await app.delete_messages(chat_id=message.from_user.id, message_ids=message.message.id)
            RUN = await SendOutToPrivateButton(message.from_user)



@app.on_message()
async def my_handler(client, message):
    global AddChannel, RemoveChannel, SendOutToPublic, SendOutToPrivate, AddedChannels, users
    
    botMe = await app.get_me()
    sender = message.from_user
    chat_id = message.text
    
    if message.from_user.id != owner or message.from_user.username != owner:
        if AddChannel == True:
            try :
                admin = False
                async for member in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
                    if member.user.id == botMe.id:
                        if chat_id not in AddedChannels:
                            AddedChannels.append(chat_id)
                        admin = True
                        break
                if admin == True:
                    await app.send_message(chat_id=sender.id, text='Channel added')
                else:
                    await app.send_message(chat_id=sender.id, text='❕ Please add me as an admin first!')
                admin = False
            except ChatAdminRequired:
                order = await app.send_message(chat_id=sender.id, text='❕ Please add me as an admin first!')
            except Exception as e:
                order = await app.send_message(chat_id=sender.id, text='❕ This username does not belongs to any channel! or am not admin on it!')
            RUN = await Keyboard(message.from_user)
            
        if RemoveChannel == True:
            try:
                AddedChannels.remove(chat_id)
                MESSAGE = ''
                for channel in AddedChannels:
                    MESSAGE = MESSAGE + '\n'+str(channel)
                order = await app.send_message(chat_id=sender.id, text=f'{MESSAGE} \n\nchannel was removed.')
            except:
                order = await app.send_message(chat_id=sender.id, text=f'This username not on list.')
            RUN = await Keyboard(message.from_user)
            
        if SendOutToPublic == True:
            await app.send_message(chat_id=sender.id, text=f'Start sending to {len(AddedChannels)} channels')
            for channel in AddedChannels:
                await app.forward_messages(chat_id=channel, from_chat_id=botMe.id, message_ids=message.id)
            await app.send_message(chat_id=sender.id, text=f'Finished. Message has been sent to {len(AddedChannels)} channels')
            RUN = await Keyboard(message.from_user)
            
        if SendOutToPrivate == True:
            await app.send_message(chat_id=sender.id, text=f'Start sending to {len(users)} users')
            for user in users:
                await app.forward_messages(chat_id=user, from_chat_id=botMe.id, message_ids=message.id)
            await app.send_message(chat_id=sender.id, text=f'Finished. Message has been sent to {len(users)} users')
            RUN = await Keyboard(message.from_user)

# RUN
app.run()