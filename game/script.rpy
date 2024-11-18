#SET CHARACTERS
define p = Character("You", color= "#df059a")
define tv = Character("Television")
define f = Character("Friend", color= "#7605df")
define fna = Character("Elder", color="#12a683")
define fnf = Character("Community Member", color="#54cd03")
define s = Character("Rceptionist", color="#0050df")
define np = Character("Council leader", color="#00bfae")
define pol = Character("Politician", color="#00ccff")
define lab_rec = Character("Receptionist", color="#ff0062")
define efor = Character("Professor Engels", color="#80ff37")
 

#SET VARIABLES
#Room variables
default bedroom_status = False
default count_drawer_Tfrontdoor = False
default count_drawer_Tfrontdoor2 = False
default current_room = 'start'
default fn_status = False
#Inventory variables
default newspaper = False
# default fn_counter = False
# default fn_for = False
# default e_counter = False
# default e_for = False
# default politician = False
#Journal variables
default journal_entries = []
default journal_open = False
#Phone system variables
define p_nvl = Character("You", kind=nvl, color= "#df059a", callback=Phone_SendSound)
define f_nvl = Character("Steve", kind=nvl, color= "#df059a", callback=Phone_ReceiveSound)
define config.adv_nvl_transition = None
define config.nvl_adv_transition = Dissolve(0.3)
#Checkpoint quiz varibles
default selected_options = []


#SET PYTHON FUNCTIONS
init python: 
    def add_to_journal(dialogue):
        # to add dialogue to the journal
        if dialogue not in journal_entries:
            renpy.notify("All written down on my journal!")
            journal_entries.append(dialogue)

    def ToggleSelected(entry):
        # Add or remove the entry from selected_options
        if entry in selected_options:
            selected_options.remove(entry)
        else:
            selected_options.append(entry)
    
    def check_answers_yes():
        # All correct points for proposition
        correct_answers = [
            "Another information bla bla"
        ]
        if sorted(selected_options) == sorted(correct_answers):
            renpy.hide_screen("yes_checkquiz")
            renpy.jump("task_passed")
        else:
            renpy.notify("Incorrect or incomplete selection. Try again.")
            selected_options.clear()  # Clear selections if incorrect

    def check_answers_no():
        # All correct points for opposition
        correct_answers = [
            "Another information bla bla"
        ]
        if sorted(selected_options) == sorted(correct_answers):
            renpy.hide_screen("no_checkquiz")
            renpy.jump("task_passed")
        else:
            renpy.notify("Incorrect or incomplete selection. Try again.")
            selected_options.clear()  # Clear selections if incorrect
#ZOOMING IMAGE
transform double_size:
    # how to use it: show image_name at double_size
    zoom 1.5
transform half_size:
    # how to use it: show image_name at double_size
    zoom 0.5


#SET SCREENS / LABELS
#Journal screen
screen journal():
    if journal_open:
        frame:
            align (0.0, 0.2) 
            xpadding 10
            ypadding 10
            xsize 400
            ysize 250

            viewport:
                draggable True
                scrollbars "vertical" 

                vbox:
                    add "journal_open.png"  xpos 0.5 xanchor 0.5 #Journal icon
                    text "Journal" xalign 0.5 bold True size 20 # Title for the journal
                    for entry in journal_entries:
                        text "✅  " + entry style "journal_entry"
#Journal toggle button screen
screen journal_toggle_button():
    imagebutton:
        action ToggleVariable("journal_open", True, False)
        idle "journal_main.png"
        hover "journal_hover.png"
        align (0.0, 0.0)
#Inventory system
label inventory_room:
    scene inventory_background
    #THESE NEED TO BE ADDED IN INSTANCE
    #$ newspaper = True
    call screen inventory_icon_room
screen inventory_icon_room:
    if newspaper:
        imagebutton:
            xanchor 0.5
            yanchor 0.5
            xpos 0.75
            ypos 0.6835
            idle "paper.png"
            hover "paper_hover.png"
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.5
        ypos 0.9
        idle "back_button.png"
        hover "back_button_hover.png"
        action Jump(current_room)


#SET STYLES
#Journal entry style
style journal_entry:
    color "#E0E0E0"
    xpadding 10
    ypadding 10
    left_margin 10
    top_margin 5
    bottom_margin 30 


#How to use journal system
# menu:
#         e "Here's some important information you might want to keep."
#         "Take a note.":
#             # Add the dialogue to the journal
#             $ add_to_journal("Another information bla bla")
#         "Skip.":
#             pass  # Do nothing if the player chooses not to keep it


#START HERE
label start:

    show screen journal_toggle_button
    show screen journal

    #Tutorial
    $ current_room = "start"
    if bedroom_status:
        scene bk_t_bedroom # with fade
        call screen bd_press
    else:
        play sound newsbroadcast
        pause 2.0 
        scene bk_t_bedroom
        with fade 
        tv "We are building a hydroelectric dam at the local river."
        "We're what?!"
        tv "Well, the city is thinking about it"
        "Damn, that really sucks."
        "I love going to the river."
        stop sound
        scene bk_river
        play music "audio/naturemusic.mp3" 
        "I spent a lot of time there with everyone."
        "Most of it was me just..."
        "Trying to get away from life by canoeing or hanging out with my friends."
        stop music fadeout 1.0
        scene bk_t_bedroom
        play sound "audio/phone_buzz.mp3"
        "Phone" "*bzt* *bzt*"
        "My phone?"
        jump phone_talking

label phone_talking:
    scene bk_t_bedroom 
    
    #Phone conversation starts here
    nvl_narrator "(⁄ ⁄•⁄ω⁄•⁄ ⁄)   (´｡• ᵕ •｡`) ♡"
    play sound "audio/ReceiveText.ogg"
    f_nvl "OMG!! Did you hear the news? The city council wants to build a dam on our river!"
    play sound "audio/SendText.ogg"
    p_nvl "No I can’t believe it, I even love to go there by myself."
    play sound "audio/ReceiveText.ogg"
    f_nvl "I guess no more canoeing, swimming, hanging out at the river."
    play sound "audio/SendText.ogg"
    p_nvl "Sadly..."
    play sound "audio/ReceiveText.ogg"
    f_nvl "Wait, you work at the town hall, right?."
    play sound "audio/SendText.ogg"
    p_nvl "Yes"
    play sound "audio/ReceiveText.ogg"
    f_nvl "So, you must have a say in this. You should do something about it."
    play sound "audio/SendText.ogg"
    p_nvl "You’re right, I’ll figure out just how important this dam is to our community."
    play sound "audio/ReceiveText.ogg"
    p_nvl "Guess I’d better dive in before this idea floods the town! Someone bring me some floaties-I’m diving in.."
    play sound "audio/ReceiveText.ogg"
    f_nvl "HAHA, good luck , well I got to go, cya."
    play sound "audio/ReceiveText.ogg"
    p_nvl "Talk to you later, bye."

    scene bk_t_bedroom
    "Alright! No more talking. Let's go exploring!!"
    $ bedroom_status = True
    call screen bd_press
   
screen bd_press:
    #door
    imagebutton:
        align(0.85, 0.36)
        idle "door.png"
        hover "door_hover.png"
        action Jump("map_fn")
    #image_frame
    imagebutton:
        align(0.47, 0.60)
        idle "image_frame.png"
        hover "image_frame_hover.png"
    #newspaper
    imagebutton:
        align(0.20, 0.72)
        idle "paper.png"
        hover "paper_hover.png"
        action SetVariable("newspaper", True)
    #folder
    imagebutton:
        align (0.0, 1.0) 
        idle "folder_main.png"
        hover "folder_hover.png"
        action Jump("inventory_room")


#FIRST NATION SCENE
label map_fn:
    $ current_room = 'map'
    scene map_background
    with fade 
    "Right, let's head to the neighborhood first to find more about how the dam affects people."
    call screen map_fn
    jump fn_room

screen map_fn:
    #neighborhood
    imagebutton:
        align(0.215, 0.175)
        idle "map_neighborhood.png"
        hover "map_neighborhood_hover.png"
        action Jump("fn_room")

label fn_room:
    $ current_room = "fn_room"
    if fn_status:
        scene fn_bksr
        "Am I ready to leave this area?"
        menu:
            "Yep!":
                jump map_en
            "Still something to do.":
                jump choicesfnstay
    else:
        scene fn_bksr
        "If I walk around I might run into some people to talk to."
        $ fn_status = True
        call screen fnsr_options

label choicesfnstay:
    $ current_room = "choicesfnstay"
    scene fn_bksr
    call screen fnsr_options

screen fnsr_options:
    #left option
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.6
        idle "arrowl.png"
        hover "arrowl_hover.png"
        action Jump("fnl")
    #right option
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.6
        idle "arrowr.png"
        hover "arrowr_hover.png"
        action Jump("fnr")    
    #folder
    imagebutton:
        align (0.0, 1.0) 
        idle "folder_main.png"
        hover "folder_hover.png"
        action Jump("inventory_room")

default been_fnl = False
default been_fnr = False

#Left arrrow: fn
label fnl:
    if been_fnl:
        scene fn_bkl
        $ current_room = "fnl"
        call screen fnl_options

    else:
        scene fn_bkl
        with fade 
        $ current_room = "fnl"
        $ been_fnl = True
        show fnaagainst at double_size
        fna "Hello and welcome."
        fna "What brings you here?"
        p "Hello, my name is Evelyn, and I'm here to ask you..."
        p "Umm.. What do you think about the plan to build a dam on the nearby river?"
        fna "Ahh, I see why you're here"
        fna "You want us to give up our land, so you..."
        fna "So you can build that dam."
        fna "Our community has right to these lands, including that river."
        fna "we will try to halt that construction no matter what."
        p "No, you misunderstood. I am just trying to learn more about your perspective."
        fna "My perspective?"
        fna "This is our land and we will not allow you to destroy it with your technology."
        p "Why do you think that a hydro-electric dam is destorying the land?"
        fna "We are not stupid."
        fna "We know all about the bad affects of the golorious hydro-electric dam"
        p "Oh really? What are they?"
        fna "There are many, where should I begin."
        fna "Our ancestors lived along these waters. The river is our life, blood and spirit."
        menu:
            "Our ancestors lived along these waters. The river is our life, blood and spirit."
            "Take a note.":
                $ add_to_journal("Our ancestors lived along these waters. The river is our life, blood and spirit.")
            "Skip.":
                pass 
        p "Interesting, please, tell me more."
        fna "Secondly, these dams drown our lands, erasing our history and future."
        menu:
            "Secondly, these dams drown our lands, erasing our history and future."
            "Take a note.":
                $ add_to_journal("Secondly, these dams drown our lands, erasing our history and future.")
            "Skip.":
                pass 
        fna "The land provides for us, and in return we protect."
        p "So, is it because of cultural reasons?"
        fna "That is right, destroying these lands for energy disregards our way of life."
        fna "Also, it's more than that."
        fna "We will lose our hunting grounds for fish and deer, that is our source of income and food."
        menu:
            "We will lose our hunting grounds for fish and deer, that is our source of income and food."
            "Take a note.":
                $ add_to_journal("We will lose our hunting grounds for fish and deer, that is our source of income and food.")
            "Skip.":
                pass
        fna "It will destroy the nature beauty of the river."
        p "So it is more than just cultural reason?"
        fna "Of course it is more than just cultural reasons."
        fna "Some people just want a dam to boost their economy."
        fna "They don't really care about the land, the water, or the skies."
        fna "That is why we will use the power of our treaties in the court of law to resist the constuction of the dam."
        p "I understand your reasoning."
        p "Thank you for helping understand your persepctive."
        fna "You're welcome, I hope you can help us stop the construction of that dam."
        p "I'll wee what I can do."
        p "Good bye."
        fna "Bye."
        call screen fnl_options
    
#         #example of how you integrate a journal system
#         fna "For some, these dams are progress. But to me, they are a means of destruction. They drown our lands, erasing our history and our future."
#         menu: 
#             "But doesn't powering our society with diesel fuel cause even more harm?":
#                 jump choicefnl1
#             "So, the land provides for you and your community, and in turn you wish to protect it?":
#                 jump choicefnl2

# label choicefnl1:
#     fna "While that may be true, the consequences of building a dam are more harmful to my community."
#     fna "You see, we lose more than just land; we lose a part of our identity. We lose our the areas where we hunt for food, for fish and deer. The result of the dam would cause flooding in our area, destroying vegetation, stripping the land of its natural resources."
#     jump fnl_choice2

# label choicefnl2:
#     fna "Yes, this is the duty my community has held since the beginning. The land provides for us, we protect it in turn. Besides we use these lands as a means to provide for ourselves."
#     jump fnl_choice2

# label fnl_choice2:
#     menu:
#         "But, there's always a different place where you can hunt... With the amount of energy required for society, don't you think we need more dams to help foster this need?":
#             jump choicefnl3
#         "So, for you, you're generally against this as it is harmful for your community's existence and because it harms your identity?":
#             jump choicefnl4

# label choicefnl3:
#     fna "It seems that you aren't listening to what I have to say."
#     fna "Then, I will kindly ask you to leave me be."
#     hide fnaagainst at double_size
#     p "That... could've gone better."
#     p "I didn't get to ask her to add her account to my journal..."
#     call screen fnl_options

# label choicefnl4:
#     fna "Yes."
#     p "Would you be willing to write that down in my notebook for me? I wish to learn all that I can about this situation."
#     fna "Of course!"
#     $ fn_counter = True
#     p "Thank you so much!"
#     fna "Well I best go back to what I was doing before, take care."
#     hide fnaagainst at double_size
#     call screen fnl_options


screen fnl_options:
    #right option
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.9
        ypos 0.6
        idle "arrowr.png"
        hover "arrowr_hover.png"
        action Jump("fn_room")    
    #folder
    imagebutton:
        align (0.0, 1.0) 
        idle "folder_main.png"
        hover "folder_hover.png"
        action Jump("inventory_room")

#Right arrow: fn
label fnr:
    scene fn_bkr
    $ current_room = "fnr"
    if been_fnr:
        scene fn_bkr
        call screen fnr_options
        # If you want to be able to return back. add discussion here.
        # p "Is there anything else I need to discuss with the community members here?"
        # menu:
        #     "Yes, let's continue the conversation.":
        #         jump fnr_dialogue
        #     "No, I think I'm done here.":
        #         jump fn_room

    else:
        scene fn_bkr
        $ been_fnr = True
        show fnafor 
        fnf "Excuse me."
        p "Yes?"
        fnf "I would like to provide my opinion on the dam."
        p "Yes, I would love to hear your opinion."
        p "What do you think about the construction of a new dam?"
        fnf "I really care about our land. But..."
        fnf "I think that the dam might be a good way to harness energy for our community."
        p "Does that mean you support building the dam?"
        fnf "Yes, I do support building the dam."
        p "Why?"
        fnf "Building the dam will provide jobs and contracts to First Nations."
        menu:
            "Building the dam will provide jobs and contracts to First Nations."
            "Take a note.":
                $ add_to_journal("Building the dam will provide jobs and contracts to First Nations..")
            "Skip.":
                pass
        fnf "This could be a really big boost to our economy."
        p "Ohh, okay."
        p "Is there any other reason?"
        fnf "Yes, the dam will remove our communities dependence on diesel oil for power."
        menu:
            "Yes, the dam will remove our communities dependence on diesel oil for power."
            "Take a note.":
                $ add_to_journal("Yes, the dam will remove our communities dependence on diesel oil for power.")
            "Skip.":
                pass
        fnf "You use diesel fuel to power your community?"
        p "Yes, we rely on it for electricity."
        p "Any power outages can last for days at a time."
        fnf "That does not sounds good."
        p "It is not."
        p "The dam will provides reliable energy."
        menu:
            "The dam will provides reliable energy."
            "Take a note.":
                $ add_to_journal("The dam will provides reliable energy.")
            "Skip.":
                pass
        p "Well, thank you for sharing that with me."
        fnf "That's all I wanted to say."
        fnf "Thanks for listening"
        p "No problem, thank you for sharing."
        fnf "Bye."
        hide fnafor
        call screen fnr_options


# label fnr_opinion_differs:
#     fnf "Well, I have the right to my own opinion, don’t I?"
#     p "Yes, of course. Please, tell me more about why you support it."

# label fnr_support_reason:
#     fnf "Building the dam will provide jobs to our people and contracts to First Nation developers."
#     fnf "This could really benefit our community economically."

#     menu:
#         "That’s something I hadn’t considered. Would you mind if I noted this down?":
#             $ add_to_journal("Community Member's perspective: The dam could bring economic benefits to the First Nation community.")
#             jump fnr_environment

#         "I see. What about the environmental impact?":
#             jump fnr_environment

# label fnr_environment:
#     p "Isn’t diesel fuel harmful to the environment?"
#     fnf "Oh, absolutely. And spills can contaminate large amounts of water."
#     p "Thank you for sharing that perspective with me."

#     menu:
#         "Take a note on the environmental impact of diesel fuel and the dam.":
#             $ add_to_journal("Diesel fuel spills can harm water sources. The dam could reduce reliance on diesel for power.")
#         "Skip taking notes.":
#             pass  

#     fnf "Thank you for taking the time to listen to me. Have a good day!"
#     p "You too, goodbye."

#     # End conversation, return to options
#     hide fnafor 
#     call screen fnr_options

screen fnr_options:
    #left option
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.6
        idle "arrowl.png"
        hover "arrowl_hover.png"
        action Jump("fn_room")
    #folder
    imagebutton:
        align (0.0, 1.0) 
        idle "folder_main.png"
        hover "folder_hover.png"
        action Jump("inventory_room")


#LABORATORY / ENV SCENE
label map_en:
    $ current_room = 'map_en'
    scene map_background
    pause 1.0
    jump text_after_first_nations
    # with fade
    # p "Right, let's head to the University of Toronto to talk to some experts about the dam."
    # call screen map_lab
    # jump lab_reception

label map_en_continued:
    $ current_room = 'map_en'
    scene map_background
    p "Right, let's head to the University of Toronto to talk to some experts about the dam."
    call screen map_lab
    jump lab_reception

label text_after_first_nations:
    scene map_background
    # nvl_narrator "(⁄ ⁄•⁄ω⁄•⁄ ⁄)   (´｡• ᵕ •｡`) ♡"
    play sound "audio/ReceiveText.ogg"
    f_nvl "They're some really smart professor at UofT that would love to chat."
    play sound "audio/SendText.ogg"
    p_nvl "Oh really, who?"
    play sound "audio/ReceiveText.ogg"
    f_nvl "A friend of mine, Professor Engels. He has a PHD in environmental studies."
    play sound "audio/SendText.ogg"
    p_nvl "Okay, I'll head there now."
    play sound "audio/ReceiveText.ogg"
    f_nvl "The address is 40 St George St."
    play sound "audio/SendText.ogg"
    p_nvl "Great."
    jump map_en_continued

screen map_lab:
    # University of Toronto lab location
    imagebutton:
        align(0.240, 0.730)
        idle "map_lab.png"
        hover "map_lab_hover.png"
        action Jump("lab_reception")

label lab_reception:
    $ current_room = 'lab_reception'
    scene backgroundlabfront
    show lab_rec with dissolve
    "I head to the front desk at the University of Toronto's Environmental Science Department."
    p "Hello"

    lab_rec "Hi, How can I assist you today?"

    p "I'm here to speak with Professor Engels. He should be expecting me."

    lab_rec "Professor Engels office is located in room 310."

    p "Thank you!"
    jump lab_professor_engels

label lab_professor_engels:
    $ current_room = 'lab_professor_engels'
    scene backgroundlab1
    show efor with dissolve
    $ pros_done = False
    $ cons_done = False
    window show

    "I knock on Professor Swift's door and enter. She's sitting at her desk surrounded by research papers."
    
    efor "Ah hello, come on in. How can I help you today?"

    p "umm, will you help me explore the benefits of a hydro-electric dam?"

    p "There is a proposal to build a new hydro-electric dam on Una river"

    efor "Yes, I would love to speak with you about the dam."
    
    efor "Shall we first talk about the pros or the cons?"

    menu:
        "Pros":
            jump efor_pros

        "Cons":
            jump efor_cons

label efor_conversation_transition:
    if cons_done == True and pros_done == True:
        $ current_room = 'lab_professor_engels'
        scene backgroundlab1
        show efor
        window show
        p "Well, thank you for telling me."
        p "I will try to make the right decision when I introduce my findings to town hall."
        efor "You're welcome and thank you for speaking with me."
        efor "I am glad you're taking the initiative to learn more about our environment."
        efor "Have a good day."
        p "You too, Bye."
        jump lab_reception2
    if next_conversation == 'pros':
        window show
        jump efor_pros
    else:
        window show
        jump efor_cons

label efor_pros:
    $ current_room = 'lab_professor_engels'
    scene backgroundlab1
    show efor
    window show
    efor "Let's consider the benefits of the dam."

    efor "You see, Hydro-electric dams provide reliable energy to communities across the globe."

    efor "The flow of water is non stop, so energy is constantly being harnessed for our use."

    p "That sounds really good."

    efor "Additionally, it is a greener alternative to fossil fuels and coal."

    p "So they want to build the dam to get rid of the use of fossil fuels and coal?"

    efor "Yes, coal and fossil fuels trap heat from escaping our atmosphere."

    efor "It causes global warming."

    p "Global warming, is that even real?"

    efor "Yes, global warming is a very concerning global crisis."

    p "Wow, I can't believe I heard one time that it was a hoax."

    efor "No it's real."

    efor "Anyways..."
    
    $ pros_done = True
    $ next_conversation = 'cons'
    jump efor_conversation_transition

label efor_cons:
    $ current_room = 'lab_professor_engels'
    scene backgroundlab1
    show efor

    efor "There are cons to building the dam."

    efor "To begin with, currently some communities rely on fossil fuels for power."

    efor "An oil spill could contaminate large amount of water, rendering it unable to drink."

    p "Oh, I didn't realise that oil spill were so bad."

    efor "They are."

    efor "Also, building a dam will disrupt an abundunce of wild life."

    efor "Approximately 1 million species are at risk of going extinct."

    p "Those poor thing, we should try and save them."

    efor "Wait... There's more."

    efor "Dam's often lead to flooding in certain areas. The decomposing of plants can release poisonuous methan gas into our air."

    efor "This can be bad for local communities."

    p "Methan gas! That is terrible."

    efor "Yes it is."

    efor "One last note." 
    
    efor "Although hydro-electric dams are a greener alternative to fossil fuels."

    efor "They unfortunately perpetuate industrialization, and provide energy at a cheaper price. Which inturn could be worse for the environment over time."

    p "Wow, so green growth isn't always greener."

    efor "Exactly."

    $ cons_done = True
    $ next_conversation = 'pros'
    jump efor_conversation_transition


    # efor "Let's consider the benefits of the dam."

    # p "So, you're suggesting the dam could be beneficial in some ways?"

    # efor "Yes, exactly. The energy it generates could help reduce carbon emissions, and flood control can protect areas prone to natural disasters. However, we also need to consider how it affects fish populations and aquatic life."

    # p "That’s helpful, thank you. I think I’ll add this information to my journal."

    # # Option to add journal entry
    # menu:
    #     "Add to journal":
    #         $ add_to_journal("Professor Swift explains the potential benefits of the dam, including renewable energy generation and flood control, but also highlights environmental concerns like biodiversity loss.")
    #         p "I’ll make sure to write this down for reference."
    #     "Don’t add to journal":
    #         p "I’ll just remember this for now."
    
    # p "Thank you for your time, Professor Swift. I’ll head back to the reception desk to check if Professor Green is available yet."

    # show arrow_left
    # jump lab_reception2

label lab_reception2:
    $ current_room = 'lab_reception'
    scene backgroundlabfront
    show lab_rec with dissolve
    window show dissolve
    "At the front desk, the secretary looks up from their computer and offers a polite smile."

    lab_rec "Heading out already? I hope your meeting went well!"

    p "Yes, it was quite informative. Thank you for your help earlier."
    
    lab_rec "Anytime. Have a great day!"

    "As I step toward the main doors, my phone buzzes in my pocket."

    play sound "audio/phone_buzz.mp3"
    f_nvl "Yo! Where are you? The politician is really interested in the dam project and is having a press conference in his office right now."

    p_nvl "The politician? I’ll have to check that out, thanks for the heads-up."

    f_nvl "I think you should meet him, he might have more information about the dam’s support from the political side."

    p_nvl "Got it, I’ll go talk to him."

    jump map_pol

    # lab_rec "I’ll let you know when Professor Green is ready to meet."

    # jump politician_call

label politician_call:
    $ current_room = 'politician_call'
    p "I quickly get in touch with Steve, and he tells me that the politician is attending a press conference at his office. It sounds like the politician is really pushing for the dam’s construction."

    f_nvl "I think you should meet him, he might have more information about the dam’s support from the political side."

    p_nvl "Got it, I’ll go talk to him."
    jump lab_reception3

label lab_reception3:
    $ current_room = 'lab_reception'
    scene backgroundlabfront
    show lab_rec with dissolve
    lab_rec "Ah, finally! Professor Green is available now. You can speak with her about the dam's impact."
    jump lab_professor_green

# label lab_professor_green:
#     $ current_room = 'lab_professor_green'
#     scene backgroundlab2 with dissolve
#     show efor at left with fade
#     p "I enter Professor Green’s office, and she looks up from her work."

#     s "Oh, hello! I’m Professor Sage. I understand you want to discuss the potential impacts of a hydro-electric dam on the Una River?"

#     p "Yes, I’d like to hear your thoughts on the downsides."

#     s "Certainly. Hydro-electric dams have significant environmental costs. They flood large areas of land, disrupting ecosystems and displacing wildlife."

#     menu:
#         "Ask about habitat disruption":
#             p "How do dams disrupt habitats?"

#             s "When land is flooded, entire ecosystems are submerged. Fish, plants, and animals lose their natural habitats."
#             s "This can lead to a loss in biodiversity, harming species that rely on the natural river environment."

#             p "That sounds serious – I hadn’t thought about it that way."

#         "Ask about pollution concerns":
#             p "Do hydro-electric dams contribute to pollution?"

#             s "Yes, indirectly. When organic material like plants decays underwater, it releases methane, a potent greenhouse gas."
#             s "Methane contributes to global warming, sometimes even more than carbon dioxide."

#             p "That’s unexpected. I thought hydro-electric power was cleaner."

#             s "Cleaner, yes, but not without environmental consequences."

#     # Continue the conversation
#     p "It seems like there’s a lot to consider. Do you believe the cons outweigh the pros?"

#     s "In many cases, yes. There are less invasive alternatives, like wind and solar, that don’t involve flooding or habitat loss."
#     s "While dams provide energy, the cost to our ecosystems can be too high."

#     menu:
#         "Add to journal":
#             $ add_to_journal("Professor Sage shared concerns about habitat destruction, methane emissions, and biodiversity loss due to hydro-electric dams.")
#             p "I’ll jot this down in my journal."

#         "Don’t add to journal":
#             p "I’ll keep this in mind for now."

#     # show arrow_left
#     jump map_pol

#POLITICIAN OFFICE
label map_pol:
    $ current_room = 'map_pol'
    scene map_background
    p "let's head to mayor to talk to him why he wants the dam."
    call screen map_office
    jump office

screen map_office:
    # office location
    imagebutton:
        align(0.787, 0.145)
        idle "map_office.png"
        hover "map_office_hover.png"
        action Jump("office")

#Office Scene (Receptionist Interaction)
label office:
    $ current_room = "office"
    scene backgroundofficefront
    p "Alright, now it's time to head to the office."
    p "I need to meet with the politician, but first, there's a receptionist I need to talk to."

    # Receptionist appears
    show office_rec with dissolve
    s "Good morning, sir. May I have your name and ID, please?"

    menu:
        "Give my government ID":
            # Show the Government ID from the inventory
            $ government_id = "phone_background.png"
            show image government_id at half_size
            p "Here is my government ID. I work for the government."

            s "Thank you, I will let the politician know you're here."
            jump office_wait

        "Refuse to give ID":
            p "I don't want to show my ID right now."

            s "I'm afraid I can't let you through without proper identification."

            # Add journal entry about refusal
            $ add_to_journal("Refused to give government ID to receptionist.")

            jump office_exit

label office_wait:
    $ current_room = "office_wait"
    scene backgroundofficefront

    p "Now I need to wait until I get to speak with the politician."

    # Wait for some time, add suspense with a short pause or change in the environment
    play music "audio/waiting_music.mp3"
    p "The office is quiet, and the tension feels thick in the air. I wonder what the politician will say."

    # Next interaction with a normal person
    show np with dissolve

    np "You know, everyone has their own thoughts on this whole dam situation."

    np "Some think it's a good idea, while others say it's not. I don't really know where I stand, honestly."

    np "But in the end, it's out of our hands. There's nothing we can do about it."

    menu:
        "Ask more about their opinion":
            np "Well, like I said, I don't really have an opinion. I just think it's something the government wants to do, and it's probably already decided."

            jump office_wait_continue

        "Stay silent and listen":
            np "Yeah... Well, no one really wants to listen to us regular folks anyway. Politicians only care about their votes."

            $ add_to_journal("Stayed silent while a normal person talked about the dam situation.")

            jump office_wait_continue

label office_wait_continue:
    # Now the player will meet the politician
    $ current_room = "office_wait_continue"
    scene backgroundoffice
    show pol with dissolve
    p "Finally, I get to meet the politician."

    # Politician starts speaking

    pol "Ah, I see you're here to discuss the dam situation. Let me tell you, it's going to be a great thing for the community."

    pol "The dam will provide us with more energy, create jobs, and boost the local economy. People don't understand how much it can benefit everyone."

    pol "I know some people are concerned about the environment, but honestly, the positives outweigh the negatives. There's a reason why this project is moving forward."

    menu:
        "Ask about environmental concerns":
            pol "The environment? Please, we're using the best technology available to ensure minimal impact. It's a small price to pay for progress."

            $ add_to_journal("Politician downplays environmental concerns and emphasizes the benefits of the dam.")

            jump office_exit

        "Agree with the politician":
            pol "I knew you would understand. We need this dam to move forward for the future of our community."

            $ add_to_journal("Politician discusses the benefits of the dam with the player.")

            jump office_exit

        "Disagree with the politician":
            pol "You're entitled to your opinion, but the decision has already been made. The dam will be built, whether you like it or not."

            # Politician becomes angry and the player can't get more information
            $ add_to_journal("Politician becomes frustrated with the player and refuses to provide more details.")

            jump office_exit

label office_exit:
    scene map_background
    p "I think it's time to head back. The meeting at the town hall is coming up, and I need to be prepared."
    jump map_town

#TOWNHALL 
label map_town:
    $ current_room = 'map'
    scene map_background
    p "Now, it is time for you to vote!"
    call screen map_tn
    jump tn_room

screen map_tn:
    #neighborhood
    imagebutton:
        align(0.785, 0.726)
        idle "map_townhall.png"
        hover "map_townhall_hover.png"
        action Jump("tn_room")

label tn_room:
    $ current_room = "town_hall"
    scene bk_townhall
    p "After gathering all the evidence, it's time to present my decision."
    p "The town hall is buzzing with discussions from all sides."
    np "Welcome to the council meeting. Today, we will vote on whether to construct The Great Ontartio Dam. Your voices will help determine the future of our community and the environment."
    call screen voting_buttons

screen voting_buttons:
    add "bk_townhall.png"
    imagebutton:
        #YES: for the dam
        align(0.25, 0.5)
        idle "yes_vote.png"
        hover "yes_vote_hover.png"
        action Show("yes_checkquiz") 

    imagebutton:
        #NO: against the dam
        align(0.75, 0.5)
        idle "no_vote.png"
        hover "no_vote_hover.png"
        action Show("no_checkquiz") 

screen yes_checkquiz:
    add "bk_townhall.png"

    # Create a frame
    frame:
        align(0.5, 0.5)
        xpadding 10
        ypadding 10
        xsize 600
        ysize 600
        
        viewport:
            draggable True
            scrollbars "vertical" 
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 10  # Space between buttons
                text "My Journal" size 30 xalign 0.5 color "#FF5733"
                for entry in journal_entries:
                    textbutton entry action [Function(ToggleSelected, entry)]
                textbutton "Check Answers" action [Function(check_answers_yes)]

screen no_checkquiz:
    add "bk_townhall.png"

    # Create a frame
    frame:
        align(0.5, 0.5)
        xpadding 10
        ypadding 10
        xsize 600
        ysize 600
        
        viewport:
            draggable True
            scrollbars "vertical" 
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 10  # Space between buttons
                text "My Journal" size 30 xalign 0.5 color "#FF5733"
                for entry in journal_entries:
                    textbutton entry action [Function(ToggleSelected, entry)]
                textbutton "Check Answers" action [Function(check_answers_no)]

label task_passed:
    p "Congratulations! You've selected the correct answers and passed the task."

label end:
    return
