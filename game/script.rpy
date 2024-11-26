#SET CHARACTERS
define p = Character("Me", color= "#df059a")
define tv = Character("Television")
define f = Character("Friend", color= "#7605df")
define fna = Character("Elder", color="#12a683")
define fnf = Character("Community Member", color="#54cd03")
define s = Character("Rceptionist", color="#0050df")
define np = Character("Council leader", color="#00bfae")
define pol = Character("Doug Ford", color="#00ccff")
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
            "Building the dam will provide jobs and contracts to First Nations.",
            "The dam will remove our communities dependence on diesel oil for power.",
            "By switching to cleaner energy source like hydro-power, we can significantly reduce greenhouse gas emissions.",
            "Oil spills contaminate water, killing wildlife and leaving entire areas without clean drinking water.",
            "With hydro-power, communities get a steady supply of energy without the dangers that come with burning coal or drilling for oil.",
            "The dam will provide Ontario with clean, renewable energy.",
            "It will help reduce emissions and meet climate targets.",
            "Modern dam designs minimize ecosystem disruption and respect traditional land use."
        ]
        correct_answer = 0
        for option in selected_options:
            if option in correct_answers:
                correct_answer = correct_answer + 1
            else:
                correct_answer = correct_answer - 1

        if correct_answer >= 3:
            renpy.hide_screen("yes_checkquiz")
            renpy.jump("ending_yes_win")
        else:
            renpy.hide_screen("yes_checkquiz")
            renpy.jump("ending_yes_fail")

    def check_answers_no():
        # All correct points for opposition
        correct_answers = [
            "Our ancestors lived along these waters. The river is our life, blood and spirit.",
            "Secondly, these dams drown our lands, erasing our history and future.",
            "We will lose our hunting grounds for fish and deer, that is our source of income and food.",
            "Dams disrupt wildlife. Rivers are home to many species, and blocking them can harm ecosystems.",
            "Dams often flood nearby areas, and decomposing plants release methane gas.",
            "Dams contribute to industrialization. They make energy cheaper, which leads to more factories and pollution.",
        ]
        correct_answer = 0
        for option in selected_options:
            if option in correct_answers:
                correct_answer = correct_answer + 1
            else:
                correct_answer = correct_answer - 1

        if correct_answer >= 3:
            renpy.hide_screen("no_checkquiz")
            renpy.jump("ending_no_win")
        else:
            renpy.hide_screen("no_checkquiz")
            renpy.jump("ending_no_fail")

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
        tv "Well, the city is thinking about it."
        "Damn, that really sucks."
        stop sound fadeout 3.0
        play music "river_flow.mp3" volume 0.2
        "I love going to the river."
        scene bk_river 
        "I spent a lot of time there with everyone."
        "Most of it was me just..."
        "Trying to get away from life by canoeing or hanging out with my friends."
        stop music fadeout 1.0
        scene bk_t_bedroom
        play sound "audio/phone_buzz.mp3"
        jump phone_talking

label phone_talking:
    play music "main_theme.mp3" volume 0.5 loop
    scene bk_t_bedroom 
    #Phone conversation starts here
    # nvl_narrator "(⁄ ⁄•⁄ω⁄•⁄ ⁄)   (´｡• ᵕ •｡`) ♡"
    nvl clear
    nvl_mode "*Bzt* *Bzt*"
    window auto
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
    stop music fadeout 3.0
   
screen bd_press:
    #door
    imagebutton:
        align(0.85, 0.36)
        idle "door_yellow.png"
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
    play music "waiting.mp3" volume 0.5 fadein 0.5 loop
    scene map_background
    with fade 
    "Right, let's head to the neighborhood first to find more about how the dam affects people."
    call screen map_fn
    jump fn_room
    stop music fadeout 4.0

screen map_fn:
    #neighborhood
    imagebutton:
        align(0.215, 0.175)
        idle "map_neighborhood.png"
        hover "map_neighborhood_hover.png"
        action Jump("fn_room")

label fn_room:
    $ current_room = "fn_room"
    play music "sad.mp3" volume 0.5 fadein 0.5
    if (been_fnl) and (been_fnr):
        jump map_en
    elif fn_status:
        scene fn_bksr
        with fade
        window show
        "Maybe I should talk to more people..."
        menu:
            "Maybe I should talk to more people...{fast}"
            "Leave":
                window hide 
                with dissolve
                jump map_en
                
            "Stay":
                window hide
                jump choicesfnstay

    else:
        scene fn_bksr
        with fade
        "If I walk around I might run into some people to talk to."
        $ fn_status = True
        call screen fnsr_options

label choicesfnstay:
    $ current_room = "choicesfnstay"
    scene fn_bksr
    if been_fnl:
        call screen fnl_options_right_only
    elif been_fnr:
        call screen fnr_options_left_only
    else:
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
    play music "sad.mp3" volume 0.5 fadein 0.4 loop
    if been_fnl:
        scene fn_bkl
        with fade
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
        p "Hello, my name is Dwayne, and I'm here to ask you..."
        p "Umm.. What do you think about the plan to build a dam on the nearby river?"
        fna "Ahh, I see why you're here"
        fna "You want us to give up our land, so you..."
        fna "So you can build that dam."
        fna "Our community has right to these lands, including that river."
        fna "we will try to halt that construction no matter what."
        p "No, you misunderstood. I am just trying to learn more about your perspective."
        fna "My perspective?"
        fna "This is our land and we will not allow you to destroy it with your engineering."
        p "Why do you think that a hydro-electric dam is destorying the land?"
        fna "We are not stupid."
        fna "We know all about the bad affects of the golorious hydro-electric dam."
        p "Oh really? What are they?"
        fna "There are many, where should I begin."
        fna "Our ancestors lived along these waters. The river is our life, blood and spirit."
        window show
        menu:
            fna "Our ancestors lived along these waters. The river is our life, blood and spirit.{fast}"
            "Take a note.":
                $ add_to_journal("Our ancestors lived along these waters. The river is our life, blood and spirit.")
            "Skip.":
                pass 
        p "Interesting, please, tell me more."
        fna "Secondly, these dams might drown our lands, erasing our history and future."
        window show
        menu:
            fna "Secondly, these dams drown our lands, erasing our history and future.{fast}"
            "Take a note.":
                $ add_to_journal("Secondly, these dams drown our lands, erasing our history and future.")
            "Skip.":
                pass 
        fna "The land provides for us, and in return we protect."
        p "So, is it because of cultural reasons?"
        fna "That is right, destroying these lands for energy disregards our way of life."
        fna "Also, it's more than that."
        fna "We will lose our hunting grounds for fish and deer, that is our source of income and food."
        window show
        menu:
            fna "We will lose our hunting grounds for fish and deer, that is our source of income and food.{fast}"
            "Take a note.":
                $ add_to_journal("We will lose our hunting grounds for fish and deer, that is our source of income and food.")
            "Skip.":
                pass
        fna "It will destroy the natural beauty of the river."
        p "So it is more than just cultural reason?"
        fna "Of course it is more than just cultural reasons."
        fna "Some people just want a dam to boost their economy."
        fna "They don't really care about the land, the water, or the air."
        fna "That is why we will use the power of our treaties in the court of law to resist the constuction of the dam."
        p "I understand your reasoning."
        p "Thank you for helping me understand your persepctive."
        fna "You're welcome, I hope you can help us stop the construction of that dam."
        p "I'll see what I can do."
        p "Good bye."
        fna "Bye."
        window hide
        call screen fnl_options

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

screen fnl_options_right_only:
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

#Right arrow: fn
label fnr:
    play music "sad.mp3" volume 0.5 fadein 0.4 loop
    scene fn_bkr
    $ current_room = "fnr"
    if been_fnr:
        scene fn_bkr
        with fade
        call screen fnr_options
    else:
        scene fn_bkr
        with fade
        $ been_fnr = True
        show fnafor 

        fnf "Excuse me." with dissolve
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
        window show
        menu:
            fnf "Building the dam will provide jobs and contracts to First Nations.{fast}"
            "Take a note.":
                $ add_to_journal("Building the dam will provide jobs and contracts to First Nations.")
            "Skip.":
                pass
        fnf "This could be a really big boost to our economy."
        p "Ohh, okay."
        p "Is there any other reason?"
        fnf "Yes, the dam will remove our communities dependence on diesel oil for power."
        window show
        menu:
            fnf "Yes, the dam will remove our communities dependence on diesel oil for power.{fast}"
            "Take a note.":
                $ add_to_journal("The dam will remove our communities dependence on diesel oil for power.")
            "Skip.":
                pass
        p "You use diesel fuel to power your community?"
        fnf "Yes, we rely on it for electricity."
        fnf  "Any power outages can last for days at a time."
        p "That does not sounds good."
        fnf "It is not."
        fnf "The dam will provides reliable energy."
        window show
        menu:
            fnf "The dam will provides reliable energy.{fast}"
            "Take a note.":
                $ add_to_journal("The dam will provides reliable energy.")
            "Skip.":
                pass
        
        p "Well, thank you for sharing that with me."
        fnf "That's all I wanted to say."
        fnf "Thanks for listening"
        p "No problem, thank you for sharing."
        fnf "Bye."
        window hide
        hide fnafor
        call screen fnr_options

    stop music fadeout 3.0

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

screen fnr_options_left_only:
    #left option
    imagebutton:
        xanchor 0.5
        yanchor 0.5
        xpos 0.1
        ypos 0.6
        idle "arrowl.png"
        hover "arrowl_hover.png"
        action Jump("fnl")
    #folder
    imagebutton:
        align (0.0, 1.0) 
        idle "folder_main.png"
        hover "folder_hover.png"
        action Jump("inventory_room")

#LABORATORY / ENV SCENE
label map_en:
    $ current_room = 'map_en'
    play music "main_theme.mp3" volume 0.5 fadein 0.3 loop
    scene map_background
    with fade
    pause 0.4
    jump text_after_first_nations
    stop music fadeout 5.0
    # with fade
    # p "Right, let's head to the University of Toronto to talk to some experts about the dam."
    # call screen map_lab
    # jump lab_reception

label map_en_continued:
    $ current_room = 'map_en'
    play music "waiting.mp3" volume 0.5 fadein 0.4 loop
    scene map_background
    p "Right, let's head to the University of Toronto Lab to talk to some experts about the dam."
    call screen map_lab
    jump lab_reception

label text_after_first_nations:
    # nvl_narrator "(⁄ ⁄•⁄ω⁄•⁄ ⁄)   (´｡• ᵕ •｡`) ♡"
    nvl_mode "*Bzt* *Bzt*" with dissolve
    play sound "audio/ReceiveText.ogg"
    f_nvl "They're some really smart professors at UofT that would love to chat." with dissolve
    play sound "audio/SendText.ogg"
    p_nvl "Oh really, who?"
    play sound "audio/ReceiveText.ogg"
    f_nvl "A friend of mine, Professor Engels. She has a PHD in environmental studies."
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
    play music "main_theme.mp3" volume 0.5 fadein 0.4
    scene backgroundlabfront
    show lab_rec 
    with dissolve
    "I head to the front desk at the University of Toronto's Environmental Science Department." with dissolve

    p "Hello"

    lab_rec "Hi, How can I assist you today?"

    p "I'm here to speak with Professor Engels. She should be expecting me."

    lab_rec "Professor Engels office is located in room 310."

    p "Thank you!"
    jump lab_professor_engels

label lab_professor_engels:
    $ current_room = 'lab_professor_engels'
    scene backgroundlab1
    with fade
    show efor with dissolve
    $ pros_done = False
    $ cons_done = False
    window show

    play sound "door_knocking.mp3"
    "I knock on Professor Engels's door and enter."

    "It looks like she is doing an experiment."
    
    efor "Ah hello, come on in. How can I help you today?"

    p "Umm, will you help me explore the effects of a hydro-electric dam?"

    p "There is a proposal to build a new hydro-electric dam on Una river"

    efor "Yes, I would love to speak with you about the dam."
    
    efor "Shall we first talk about the pros or the cons?"

    menu:
        efor "Shall we first talk about the pros or the cons?{fast}"
        "Pros":
            jump efor_pros

        "Cons":
            jump efor_cons

label efor_conversation_transition:
    if cons_done == True and pros_done == True:
        $ current_room = 'lab_professor_engels'
        play music "waiting.mp3" volume 0.5 loop
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
    
    efor "Let's talk about why hydro-electric dams are so important."

    efor "To begin with, dams can replace fossil fuels as a primary source of energy."

    p "Why is that such a big deal?"

    efor "Sources of energy like fossil fuels and coal, have several serous problems."

    efor "They trap heat in our atmosphere, which contributes to global warming."

    p "Oh, I've heard about global warming. Is it really that bad?"

    efor "Yes, it's a global crisis." 
    
    efor "By switching to cleaner energy source like hydro-power, we can significantly reduce greenhouse gas emissions."
    
    menu:
        efor "By switching to cleaner energy source like hydro-power, we can significantly reduce greenhouse gas emissions.{fast}"
        "Take a note.":
            $ add_to_journal("By switching to cleaner energy source like hydro-power, we can significantly reduce greenhouse gas emissions.")
        "Skip.":
            pass

    efor "Another issue with fossil fuels are oil spills."

    efor "Oil spills contaminate water, killing wildlife and leaving entire areas without clean drinking water."
    
    menu:
        efor "Oil spills contaminate water, killing wildlife and leaving entire areas without clean drinking water.{fast}"
        "Take a note.":
            $ add_to_journal("Oil spills contaminate water, killing wildlife and leaving entire areas without clean drinking water.")
        "Skip.":
            pass
    
    p "So dams would mean no more oil spills?"

    efor "Exactly. Instead of relying on fossil fuels, hydro-electric dams harness the constant flow of water to generate energy."

    p "Reliable energy sounds great. Fossil fuels don't seem so reliable with all the risks."

    efor "With hydro-power, communities get a steady supply of energy without the dangers that come with burning coal or drilling for oil."
    
    menu:
        efor "With hydro-power, communities get a steady supply of energy without the dangers that come with burning coal or drilling for oil.{fast}"
        "Take a note.":
            $ add_to_journal("With hydro-power, communities get a steady supply of energy without the dangers that come with burning coal or drilling for oil.")
        "Skip.":
            pass

    p "Yes, it's cleaner and more sustainable."

    efor "Anyways..."
    
    $ pros_done = True
    $ next_conversation = 'cons'
    jump efor_conversation_transition

label efor_cons:
    $ current_room = 'lab_professor_engels'
    scene backgroundlab1
    show efor
    window show
    efor "There are downsides to building the dam."

    efor "For one.."
    
    efor "Dams disrupt wildlife. Rivers are home to many species, and blocking them can harm ecosystems."
    
    menu:
        efor "Dams disrupt wildlife. Rivers are home to many species, and blocking them can harm ecosystems.{fast}"
        "Take a note.":
            $ add_to_journal("Dams disrupt wildlife. Rivers are home to many species, and blocking them can harm ecosystems.")
        "Skip.":
            pass

    p "I didn’t think about how it would affect animals."

    efor "Yes. Many species could lose their habitats and be at risk of extinction."

    efor "Another issue is flooding."
    
    efor "Dams often flood nearby areas, and decomposing plants release methane gas."
    
    menu:
        efor "Dams often flood nearby areas, and decomposing plants release methane gas.{fast}"
        "Take a note.":
            $ add_to_journal("Dams often flood nearby areas, and decomposing plants release methane gas.")
        "Skip.":
            pass

    p "Methane gas? That sounds dangerous."

    efor "It is. Methane is a powerful greenhouse gas that’s harmful to the environment."

    efor "Lastly,"
    
    efor "Dams contribute to industrialization. They make energy cheaper, which leads to more factories and pollution."
    
    menu:
        efor "Dams contribute to industrialization. They make energy cheaper, which leads to more factories and pollution.{fast}"
        "Take a note.":
            $ add_to_journal("Dams contribute to industrialization. They make energy cheaper, which leads to more factories and pollution.")
        "Skip.":
            pass

    p "So even though they’re greener, they can cause long-term harm?"

    p "It seems like Dams solve some problems but create others."
    
    efor "Exactly."

    $ cons_done = True
    $ next_conversation = 'pros'
    jump efor_conversation_transition

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
    lab_rec "Ah, finally! Professor Green is available now. You can speak with  about the dam's impact."
    jump lab_professor_green


#POLITICIAN OFFICE
label map_pol:
    play music "waiting.mp3" volume 0.5 fadein 0.4
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
    play music "main_theme.mp3" volume 0.5 fadein 0.4
    scene backgroundofficefront
    with fade
    "I need to meet with the politician, but first, there's a receptionist I need to talk to."

    # Receptionist appears
    show office_rec with dissolve
    s "Good morning, sir. May I have your name and ID, please?"

    "If I want to speak with the politican, I should give  my ID."

    menu:
        "If I want to speak with the politican, I should give  my ID. {fast}"
        "Give my government ID":
            # Show the Government ID from the inventory
            $ government_id = "government_id.png"
            show image government_id at half_size
            p "Here is my government ID. I work for the government."

            s "Thank you, I will let the politician know you're here."
            jump office_wait

        "Refuse to give ID":
            p "I don't want to show my ID right now."

            s "I'm afraid I can't let you through without proper identification."
            jump map_town

label office_wait:
    $ current_room = "office_wait"
    play music "waiting.mp3" volume 0.5 fadein 0.4
    scene backgroundofficefront

    "Now I need to wait until I get to speak with the politician."

    # Wait for some time, add suspense with a short pause or change in the environment

    "The office is eerily quiet, with only the faint ticking of a clock on the wall"

    "I wonder, what will the politician say?"

    # Next interaction with a normal person
    show env_guy with dissolve

    np "You know, everyone has their own thoughts on this whole dam situation."

    np "Some think it's a good idea, while others say it's not. I don't really know where I stand, honestly."

    np "But in the end, it's out of our hands. We should try to make the right decision."

    menu:
        "Ask more about their opinion":
            np "Well, like I said, I don't really have an opinion. I just think it's something the government wants to do, and it's probably already decided."

            jump office_wait_continue

        "Stay silent and listen":
            np "Yeah... Well, no one really wants to listen to us regular folks anyway. Politicians only care about their votes."

            jump office_wait_continue
    stop music fadeout 3.0

label office_wait_continue:
    # Now the player will meet the politician
    $ current_room = "office_wait_continue"
    play music "main_theme.mp3" volume 0.5 fadein 0.4 loop
    scene backgroundoffice
    show pol with dissolve
    window show
    p "Hello, Mr. Ford."

    pol "Good afternoon. How can I help you?"

    p "My name is Dwayne, and I'd like to ask about the hydroelectric dam proposal on Una River."
    p "Why do you want to build it?"

    pol "It's a big project, and it will cost a lot, but it's an investment in our future"

    p "If it's so expensive, why is it worth building?"

    pol "The dam will provide Ontario with clean, renewable energy."

    menu:
        pol "The dam will provide Ontario with clean, renewable energy.{fast}"
        "Take a note.":
            $ add_to_journal("The dam will provide Ontario with clean, renewable energy.")
        "Skip.":
            pass
    
    pol "It will help reduce emissions and meet climate targets."
    
    menu:
        pol "It will help reduce emissions and meet climate targets.{fast}"
        "Take a note.":
            $ add_to_journal("It will help reduce emissions and meet climate targets.")
        "Skip.":
            pass

    pol "This project shows we're serious about climate leadership."

    p "So it's about moving away from fossil fuels?"

    pol "Precisely. Many communities still rely on diesel fuel, which is harmful and unreliable."

    pol "The dam will replace that with a sustainable energy source."

    p "Are there any other benefits?"

    pol "Yes. Building the dam will create jobs and boost local economies."
    
    pol "In northern and rural Ontario, it will drive development in underutilized areas."
    
    pol "It will also stabilize electricity costs for both businesses and households."

    p "That sounds helpful for the economy. What about the environment?"

    pol "We’re working closely with Indigenous communities to ensure environmental protections."
    
    pol "Modern dam designs minimize ecosystem disruption and respect traditional land use."
    
    menu:
        pol "Modern dam designs minimize ecosystem disruption and respect traditional land use..{fast}"
        "Take a note.":
            $ add_to_journal("Modern dam designs minimize ecosystem disruption and respect traditional land use.")
        "Skip.":
            pass
    
    pol "This project supports reconciliation and responsible development."

    menu:
        "Hmm, what should I say..."
        "I can't believe anything you say":
            hide pol
            show pol_angry
            pol "What is that suppose to mean?"
            p "You pretend like everything is perfect in your world."
            p "You refuse to acknowledge their could be bad to hydro-electric dams."
            pol "Though there are valid concerns, the economic and environmental benefits of this dam are too significant to ignore."
            pol "Please leave my office. I am very busy."
            jump map_town
            window hide

        "So it’s about clean energy, jobs, and working with Indigenous communities?":
            pol "Exactly. The dam will benefit Ontario in many ways."
    
            pol "It’s about securing a sustainable and affordable future for everyone."

            p "Thank you for explaining."

            pol "I hope the community sees the benefits too."

            p "Goodbye."

            pol "Goodbye, and thank you for asking the important questions."
            jump map_town
            window hide

    jump map_town

#TOWNHALL 
label map_town:
    play music "waiting.mp3" volume 0.5
    window hide
    $ current_room = 'map'
    scene map_background
    with fade 
    play sound "townhall_bell.mp3"
    "It's time to vote." with dissolve
    "Go to town hall."
    call screen map_tn
    jump tn_room

screen map_tn:
    #neighborhood
    imagebutton:
        align(0.783, 0.723)
        idle "map_townhall.png"
        hover "map_townhall_hover.png"
        action Jump("tn_room")

label tn_room:
    window hide
    $ current_room = "town_hall"
    scene bk_townhall
    play sound intersteller
    if journal_entries == []:
        $ journal_entries.append('I have no evidence to support my decision.')
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
                xsize 600  # Ensure the viewport matches the frame size for proper alignment
                ysize 0
                xalign 0.5
                yalign 0.5
                spacing 10  # Space between buttons
                null height 15
                text "My Journal" size 30 xalign 0.5 color "#FF5733"
                textbutton "Check Answers" action [Function(check_answers_yes)] xalign 0.5
                for entry in journal_entries:
                    hbox:
                        null width 25
                        $ color = "#00FF00" if entry in selected_options else "#FFFFFF"
                        textbutton entry action Function(ToggleSelected, entry) text_color color
                    # textbutton entry action [Function(ToggleSelected, entry)]

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
                xsize 600  # Ensure the viewport matches the frame size for proper alignment
                ysize 0
                xalign 0.5
                yalign 0.5
                spacing 10  # Space between buttons
                null height 15
                text "My Journal" size 30 xalign 0.5 color "#FF5733"
                textbutton "Check Answers" action [Function(check_answers_yes)] xalign 0.5
                for entry in journal_entries:
                    hbox:
                        null width 25
                        $ color = "#00FF00" if entry in selected_options else "#FFFFFF"
                        textbutton entry action Function(ToggleSelected, entry) text_color color
                # textbutton "Check Answers" action [Function(check_answers_no)]

# Here are some of the labels for the endings! Just make sure to connect these to the game :)
label ending_yes_win:
    play sound "Clapping" volume 0.2
    #dam built
    play music "main_theme" volume 0.2 fadein 0.4
    show black
    "After learning so much about the consequences of dam construction."
    "I thought it would be for the best if the dam were to be built."
    "Turns out, the city council was impressed by my argumentation."
    "And agreed with most of my points and evidence."
    "So they decided to build the dam."
    # So I don't really know everyone who's against the dam construction but if i"m missing one, feel free to add it.
    show fnaagainst
    fna "I had a feeling that the dam would have been built."
    fna "..."
    fna "Listen."
    fna "While I\'m not very happy with your decision, I can't entirely blame you can I?"
    fna "Life will become more difficult for my community because of your choice."
    fna "I hope you\'re happy."
    jump end

label ending_yes_fail:
    #dam not built
    show black
    "After learning so much about the consequences of dam construction."
    "I thought it would be for the best if the dam were to be built."
    "However, the city council wasn't convinced by my argumentation."
    "Turns out not paying attention to what people say has consequences..."
    "The council decided to not build the dam instead."
    show fnafor
    fnf "I guess I\'ll just stick to working far from my community."
    p "Why exactly do you need to do that?"
    fnf "I was counting on the dam being built, on there being more jobs closer to home."
    fnf "That would have been the best outcome for me and my family."
    p "I\'m sorry."
    fnf "It\'s not your fault. Really. I don\'t blame you."
    fnf "Just... Next time you ask for other people\'s opinions."
    fnf "Maybe listen to them properly?"
    hide fnafor
    show pol
    pol "I\'ll be real honest."
    pol "I\'m not exactly happy with this outcome."
    pol "But at the very least, you tried."
    hide pol
    jump end

label ending_no_win:
    #dam not built
    show black
    "After learning so much about the consequences of dam construction."
    "I thought it would be for the best if the dam were not to be built."
    "Turns out, the city council was impressed by my argumentation."
    "And agreed with most of my points and evidence."
    "So they decided not to build the dam."
    show pol
    pol "I had a feeling that letting you into my office was a mistake."
    pol "I had confidence in you. I believed that you could do this ONE thing for me."
    pol "Now because of you, I need to figure out different ways to meet out climate targets."
    pol "Thanks a lot for that."
    pol "I don't have time for this anymore. Goodbye."
    hide pol

label ending_no_fail:
    #dam built
    show black
    "After learning so much about the consequences of dam construction."
    "I thought it would be for the best if the dam were not to be built."
    "However, the city council wasn't convinced by my argumentation."
    "Turns out not paying attention to what people say has consequences..."
    "The council decided to build the dam instead."
    show fnaagainst
    fna "I had a feeling that the dam would have been built."
    fna "..."
    fna "Listen."
    fna "While I'm not very happy with your decision, I can't entirely blame you can I?"
    fna "Life will become more difficult for my community because of your choice."
    fna "I HOPE you're happy."
    hide fnaagainst
    jump end

label end:
    return
