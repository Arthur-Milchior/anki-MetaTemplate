"""Copyright: Arthur Milchior arthur@milchior.fr
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
Feel free to contribute to this code on https://github.com/Arthur-Milchior/anki-MetaTemplate

A Meta Template for card's type (aka blueprient, templates)


WARNING: NEVER check for empty cards until you did apply metaTemplate to every note type where you want to use it. Otherwise, you risk to delete cards which are not supposed to be empty, but which are because the {{tags}} does not appear in the front of cards.

In general, do a backup of your data BEFORE trying this addon, if either the add-on or you made a mistake, it would avoid data loss.

Usage: 
I did realize that, given a note type, all of its card type are really similar. And usually, if I want to do an edition, I want to do it to (almost) every card types.
Instead of doing copy-paste each time I want to do a small edit to each card's type, I created this add-on to edit multiple card's type at once.

I first give examples, I'll give the complete formal explanation below.
==========Basic usage===========
Add to your css.:
/*[[var||value]]*/
Add to some card's type front/back:
<span MT="var"/>

In the browser, uses edit>metaTemplate. You'll see that
<span MT="var"/>
has been replaced by
<span MT="var">value</span MT="var">

If now you change "value" for "valuation" in the css, and do edit>metaTemplate, you'll see that every 
<span MT="var">value</span MT="var">
became 
<span MT="var">valuation</span MT="var">

Note that, if you have made change between <span MT="var"> and </span MT="var">, this change has now been lost. Always do your edit either in the CSS part, or in the part which is not enclosed by MetaTemplate's tag.

you can also use edit>clean metaTemplate to have 
<span MT="var"/> 
back.
(This option allows to remove the part copied from CSS to front/back. It helps to edit, review your code.)
=============Recursive usage
Now add to the css:
/*[[var||{{#definition}}<span MT="foo" />{{/definition}}]]*/
/*[[foo||{{definition}}]]*/
(note that 
/*[[var||{{#definition}}<span MT="foo" />{{/definition}}]]
[[foo||{{definition}}]]*/
is also valid. In fact, you need just /* and */ to enclose your definition. This part means that it is code which is not really css. /* and */ will now be avoided in future examples.)

and add to some card's type front/back:
<span MT="var" /> 
Apply MetaTemplate. 

<span MT="var" /> 
is replaced by
{{#definition}}<span MT="foo" />{{/definition}}
which itself is replaced by
{{#definition}}{{definition}}{{/definition}}

This is not very useful by itself, but becomes important using the following option
=============Asking a part of the template
Now add to the css:
/*[[var||{{#definition}}<span MT="foo" />{{/definition}}]]*/
/*[[foo||{{definition}}||Definition ?]]*/

<span MT="var" /> 
is still replaced by
{{#definition}}{{definition}}{{/definition}}

However, add to some card's type front/back:
<span MT="var" asked="foo"/> 
Apply MetaTemplate. 

<span MT="var" asked="foo"/> 
is replaced by
{{#definition}}<span MT="foo" />{{/definition}}
which itself is replaced by
{{#definition}}Definition ?{{/definition}}
in the question side and by:
{{#definition}}{{definition}}{{/definition}}
in the answer side


As you can see, <span MT="foo" /> is replaced by the third element, and not the second one. This is because a metaTemplate called before stated that "foo" is "asked". 
I.e. the first element is the name of the field, the second element is its default value. The third is the question to ask instead of the important information.
===============Prefix/suffix
In the previous example: var is used to enclose foo between {{#definition}} and {{/definition}}. Instead, there is an easier way, just do:
 
[[foo||{{#definition}}||{{definition}}||Definition ?||{{/definition}}]]
In this case 
<span MT="var" asked="foo"/> 
is replaced by
{{#definition}}Definition ?{{/definition}}
in the question side and
{{#definition}}{{definition}}{{/definition}}
in the answer side


In general, if there are at least three fields (not counting the name), the first one is the prefix.
If there are at least four fields, the last one is the suffix.

====CSS classes
[[def||{{#definition}}||Definition: <<{{definition}}>>||<<Definition ?>>||{{/definition}}]]

Here <<>> is replaced by an enclosing span with classes:
-def, 
Furthermore, in "def" occured in an "asked" field in a metatemplate which led to a call of def, then the classes are also:
-asked
-asked_def

Adding def is just a matter of writing quickly something I do use often.
Adding asked allows me to use a css class on elements which are asked. And more precisely, to add it on the important part of those elements. Here, it is not usefull to add it to "Definition:" since the definition is the important part.
asked_def allows me to have a class which is applied only on asked elements and which differs according to the meta template.

Note that << and >> may also occurs in prefix and suffix. 
[[def||{{#definition}}<<||Definition: {{definition}}||Definition ?||>>{{/definition}}]]
would be perfectly valid if you want the classes to be applied to "Definition:" too.
====Adding CSS style in MetaTemplate
If you want to add <style>foo</style> in a metaTemplate, use <css>foo</css> instead. In the card's type <css> tag will be replaced by <style> tag

===Hiding
Sometime, one may wish to state in a metaTemplate A that, another metaTemplate B, .., Z should not be shown, contrary to what happens normally when A is called. One should add the field hide="B-...-Z", as in <span MT="foo" hide="B-C"/>

====Conditional mustaches
If you have conditional mustaches (i.e. {{#foo}}{{/foo}} or {{^foo}}{{/foo}}) inside a meta template, and that this template is called inside another conditional mustache, the inner conditional mustache is removed. If both conditions are similar, the content is preserved. Otherwise if the conditionals are contradictory (i.e. {{#foo}}{{^foo}}content{{/foo}}{{/foo}}) then the content is also removed. This allow to avoid error message by anki. 

=====Debugging
If, as me, you use metaTemplate a lot, you will certainly have bugs, codes which is not exactly as you want it. 
To debug it, you can  "=debug=" to your css. In this case, span metatemplate remains even when they are useless (i.e. when they occur from the application of another metatemplate), and you'll have html comment stating which conditional mustaches are contradictory/redundant. And, in each application, which field of the entry is used (i.e. prefix, default, question_asked, suffix..., see below for the full list of possibility.)

You should compile without this option before synchronizing. This option may create really huge card's type. In particular, I created cards so big that ankidroid could not handle it.

==============More controls
After ||, you may add =fieldName=, to state that the content is not the usual one.
For example [[page||=question=||=answer=Page {{page}}]] allows you to state that a "page" meta template must be removed in question side, and is Page {{page}} in the answer side. I use this since knowing the page from which a note comes may be really useful to check in my books, if I fear the note have a mistake. But I don't want to see it on the question side since it my gives a hint about the kind of answer one may expect.

Note that in this case =question= or =default= is mandatory, because MetaTemplate must know which value to use on the question side.

The possible values are:
=prefix=, =suffix=: self described
=default=, what should be used assuming there is nothing more precise
=question= what should be shown on question side
=answer= what should be shown on answer side
=asked= what should be shown if the current MetaTemplate's name is asked (i.e. belong to an "asked" field in an enclosing meta template)
=notAsked= what should be shown if the current MetaTemplate's name is NOT asked
=asked_question= what should be shown in the QUESTION side, when the current metaTemplate is asked
=asked_answer= what should be shown in the ANSWER side, when the current metaTemplate is asked
=notAsked_question= what should be shown in the QUESTION side, when the current metaTemplate is NOT asked
=notAsked_answer= what should be shown in the ANSWER side, when the current metaTemplate is NOT asked

In the case where many entry may apply, isAsked_isQuestion/Answer has the priority. isAsked is used if the previous one is not defined, then isQuestion/Answer, and finally default. Here "isAsked" represents either "asked" or "notAsked" and isQuestion/Answer  represents "answer" or "question"
===============Technical note:
As always, a few problem may arise when the HTML is not valid.
In order to accept template with unbalanced tag, I choosed the following compromise. The tag ending a <span MetaTemplate='name'> is the first </span MetaTemplate='name'>. This should cause no problem since a template should not be called inside itself. And it avoids to consider balancing of tags.

XML is not respected here. MetaTemplate should appear directly after the word span, otherwise it is not recognized. Some spaces are tolerated, but this tolerance may potentially disappear during an update. The span tag was used in order to ensure that the tag as no effect when considered in the html viewer
"""

#comment for the coder:
"""
========================
===Lexic:
============
#Entry Pattern: an element of the form [[name||=fieldName1=value1||...||=fieldNameN=value n]] (=fieldNameI= is facultative)

#Entry: the association from name to the values, as defined in one or many entry pattern. (Note that using many entry pattern with the same name will cause a warning but, hopefully, it may works)

#dictionnary:
the association from each name to its entry, as defined above.

#fieldName: is composed of letters and _ only. They should be "prefix", "suffix", "default", ("a", "q", and "a_q"; where a is either "asked" or "notAsked" and q is either "question" or "answer") 

-The prefix exists if there is at least 3 values, in this case it is the first value
-The suffix exists if there is at least 4 values, in this case it is the first value
-The default values exists, and it is the first value if there are 1 or 2 values, and the 2nd value otherwise
-The question_asked exists, and it is the second value if there are 2 values, and the third one if there are at least 3 values

The value can contains metaTag, as defined below. Be aware that you should avoid having infinite loops (a value containing its name, or containing another value which contains another value ... which contains itself). Hopefully, if you do this, you should just see an error message, but I make no promise.


#MetaTag: of the form <span MetaTemplate='name' asked='name2' hide='...' .... />, with asked and hide facultative, potentially containing multiple elements separated by "-". Using "MetaTemplate" button in the browser, this template is replaced by
<span MetaTemplate='name'>content</span MetaTemplate='name'> 

content is decided as follows:
If name appear in the hide of an enclosing metaTag, content is empty (and in fact, the span is removed)
If there is no entry for name, content is an error message
If there is an entry for name, the values of the fields a_q, a, q, and "default" are tried in this order, until one such value exists. a being asked or notAsked, depending on whether name appear in the asked field of an enclosing metaTag. q is question or answer, according to the side of the card. If fields prefix and/or suffix exists, they are appended to content. If content contains <<

If the value (concatened with prefix and suffix) contains <<foo>>, it is replaced by <span class=''>foo</span> where the classes are the name of the current entry, "asked" or "notAsked" according to whether the current template is used as a question, and "(not)asked_name". This allows to use css's class on this part of the entry, and to decide whether css must apply on question, on answer, or on both sides.





===============TODO
add the buttons in the card layout instead of the browser. It is not done because I don't have a clue about how to reload the content of the text fields of cards layout once the potential button is clicked

"""


import pprint
import cgi, sys
import re
from anki.notes import Note
from aqt.utils import tooltip, showWarning, askUser, showInfo
import aqt
from aqt import mw
from aqt.qt import *
from aqt.clayout import CardLayout
from anki.hooks import addHook

flag = re.MULTILINE | re.DOTALL

########################
#Question/answer analysis#
#################

#Templates for reading question/answer
metaTemplateField = r"""\b(MetaTemplate|MT)\s*=\s*['"](?P<name>[^'"]*)['"]"""
askedField= r"""(?:\b(?:cloze|asked|question)s?\s*=\s*['"](?P<askeds>[^'"]*)['"])"""#todo: remove |question
hideField= r"""(?:\bhides?\s*=\s*['"](?P<hide>[^'"]*)['"])"""
facultativeFields= r"""(?:"""+hideField+r"""|"""+askedField+r"""|[^/>])*"""

prefix = r"""<\s*span(?P<span>\s+"""+metaTemplateField+facultativeFields+r""")"""
enclosingSuffix = r""">.*?<\s*/\s*span\s+(MetaTemplate|MT)\s*=\s*['"](?P=name)['"].*?>"""
simpleSuffix = r"""/\s*>"""

metaTemplateHTML=prefix+r"(?:"+enclosingSuffix+r"|"+simpleSuffix+r")"#MetaTemplate
#Template for conditional, to remove test inside of test
condRegex = r"{{(?P<kind>#|\^)(?P<condName>[^}]+)}}(?:<!-----[^>]*-->)?(?P<value>.*?){{/(?P=condName)}}"#(?:<!-----[^>]*-->)? used to remove new #name; added by debuging
#Entire regexp analysis
allRegex=r"(?:"+condRegex+r"|"+metaTemplateHTML+")"#all which can be found in question/answer


#####################
#CSS analysis#
#################
# cssParamRegexp =r"""(?:\s*\|\|\s*(?:=(?P<paramName>\w*)=)?(?P<paramValue>(?:(?!\|\|)(?!]]).)*))"""
# cssParamsRegexp = r"""(?:"""+cssParamRegexp+r"""*)"""
cssRegexp= r"""\[\[\s*(\w+)\s*\|\|((?:(?!]]).)*)]]"""


def defaultValues(l):
    if l==0:
        return {}
    if l==1:
        return  {0:"default"}
    if l==2:
        return {0:"default",
                1:"asked_question"}
    if l==3:
        return {0:"prefix",
                1:"default",
                2:"asked_question",
        }
    if l>3:
        return {0:"prefix",
                1:"default",
                2:"asked_question",
                l-1:"suffix"
        }

def warning(t):
    #sys.stderr.write(t+"\n")
    pass
    
def entryFromMT(mt, name,entry=None):
    entriesPattern=mt.split("||")
    default=defaultValues (len (entriesPattern))
    if entry is None:
        entry={}
    for idx, entryPattern in enumerate(entriesPattern):
        (field,entryPattern)=re.match("^(?:=(?P<field>\w+)=)?(?P<entryPattern>.*)$", entryPattern,flags=flag).group("field","entryPattern")
        if not field:

            if idx in default:
                field= default[idx]
            else :
                showWarning(name+":"+str(idx)+" not given in an entry of length "+str(len(entriesPattern))+"\n-----\n The values are"+ str(default))
        if field in entry:
            showWarning(name+"["+field+"] already in dic")
        entry[field]=entryPattern
    return entry
            
def createDic(css):
    global dic
    """The dictionnary indicated by this template. 

    The input is css code. The dictionnarry should be in the comment
    part. If a value is defined multiple time, last definition wins"""
    css=re.sub(r"<(/?)css>",r"<\1style>",css,flags=flag)
    css=re.sub(r"MetaTemplate=",r"MT=",css,flags=flag)
    dic = {}
    double = []
    tooMuch=[]
    for (name,entryPattern) in re.findall(cssRegexp,css,flags=flag):
        #if debugMetaTemplate : showWarning("Considering entry "+name)
        if entryPattern in dic:
            double.append(entryPattern)
            entry=dic[name]
        else:
            entry ={}
        entry=entryFromMT(entryPattern,name,entry)
        dic[name]=entry
    return dic


############################

def addSpan(cssClass,replacing):
    for css in reversed(cssClass):
        replacing= "<span class='"+css+"'>"+replacing+"</span>"
    return replacing

def dicToString(dic):
    st=""
    for key,values in dic.items():
        st+="\n"+key+": "+values
    return st

##################
#Add
nonExistingMeta= set()

class Found(Exception):
    def  __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)

def applyTemplate(template, isQuestion, enclosedIn=frozenset(),askeds=frozenset(),hide=frozenset(),assumedTrue=frozenset(),assumedFalse=frozenset()):
    global clean, dic, debugMetaTemplate, clean
    """return the template, modified using the rules as follows.

    Concerning conditions:
    if {{#name}} is enclosed in {{#name}} or name in assumedTrue, the second one is removed. Similarly for ^ ^ and assumedFalse
    if {{#name}} is enclosed in {{^name}} or name is assumedFalse, the second one and its content are removed. Similarly for ^ and # and assumeTrue

    Concerning MetaTemplate tags
    If "clean" then each MetaTemplate's tag are empty if it has a closing tag with same MetaTemplate argument.
    Otherwise:
    in a MetaTemplate whose name belongs to hide, this tag is empty.
    otherwise:
    it is replaced by dic[name][isAsked_isQuestion] if it exists, otherwise by dic[name][isAsked], by dic[name][isQuestion], by dic[name]["default"] or by an error message. Here, isAsked is either "notAsked" or "asked" depending on whether asked appeared above. isQuestion is either "question" or "answer". The result is preceded by the prefix and the suffix is appended, assuming they exist.
    
    if =debugMetaTemplate= occurs in css, long message are put, to help debugMetaTemplate the MetaTemplate


    Argument of MetaTemplate or of the span tag should not contains a ' or a "

    keyword arguments:
    isQuestion -- "question" or "answer"
    askeds -- the set of askeds found in enclosing metaTemplate
    hide -- the set of hide found in enclosing metaTemplate
    assumedTrue -- the set of name, when we are in an enclosing #name
    assumedFalse -- the set of name, when we are in an enclosing ^name
    clean -- whether the result should be cleaned
    enclosedIn -- the MT seen above
    """
    def subFun(matchObject):
      try:
        global nonExistingMeta
        (span)= matchObject.group("span")
        ###########The case of metaTemplate
        if span:
            span=re.sub(r"questions?=","askeds=",span,flags=flag)
            (name,newAskeds,newHide)= matchObject.group("name","askeds","hide")
            localAskeds = askeds
            if newAskeds:
                for n in newAskeds.split("-"):
                    localAskeds = localAskeds | frozenset([n])
                    if n not in dic:
                        nonExistingMeta.add(n)
            localHide =hide
            if newHide:
                for n in newHide.split("-"):
                    localHide = hide | frozenset([n])
                    if n not in dic:
                        nonExistingMeta.add(n)

            if clean:
                raise Found( "<span"+span+"/>" )
            if name in localHide:
                 if debugMetaTemplate:
                     raise Found( "<span"+span+"/><!---Previous MetaTemplate hidden-->)" )
                 else:
                     raise Found ("")
            if name not in dic:
                nonExistingMeta.add(name)
                raise Found( "<span"+span+">Error: "+name+" does not exists"+"</span MetaTemplate='"+name+"'>")
            if name in localAskeds:
                isAsked="asked"
            else:
                isAsked="notAsked"
            
            for field in [isAsked+"_"+isQuestion,isAsked,isQuestion,"default"]:
                if field in dic[name]:
                    if name in enclosedIn:
                        if not askUser(name+" inside itself"):
                            raise Exception
                    entry = dic[name]
                    content = entry[field]
                    content=entry.get("prefix","<!-- no prefix -->" if debugMetaTemplate else "")+content+entry.get("suffix","<!-- no suffix -->" if debugMetaTemplate else "")
                    content=re.sub(r">>",r"</span>",content)
                    content=re.sub(r"<<",(r"<span class='"
                                        +((name+" "+isAsked+"_"+name+" ")if name else "")
                                        +isAsked+"'>"),content)
                    content=applyTemplate(content,isQuestion,(enclosedIn|frozenset([name])) ,localAskeds,localHide,assumedTrue,assumedFalse)
                    if debugMetaTemplate:
                       content = "<!--"+field+"--->"+content
                    if debugMetaTemplate or (not enclosedIn):
                        content = "<span"+span+">"+content+"</span MetaTemplate='"+name+"'>"
                    raise Found( content)
            nonExistingMeta.add(name+"::"+isAsked+"_"+isQuestion)
            raise Found( "<span"+span+">Error: "+name+" not found for"+isAsked+"_"+isQuestion+"</span MetaTemplate='"+name+"'>" if debugMetaTemplate else "<span"+ span+"/>")


        #####Considering conditional mustaches
        (kind,condName,value)= matchObject.group("kind","condName","value")
        assert kind
        if (condName in assumedFalse and kind=="#") or (condName in assumedTrue and kind=="^"):
            if enclosedIn:
                raise Found( "<!----- Contradiction regarding "+kind+condName+"-->" if debugMetaTemplate else "")
            else:
                raise Found( "Contradiction regarding "+kind+condName+"at top level" if debugMetaTemplate else "")
        if (condName in assumedFalse and kind=="^") or (condName in assumedTrue and kind=="#"):
            if enclosedIn:
                raise Found( (("<!----- useless "+kind+condName+"-->" if debugMetaTemplate else "")+applyTemplate(value,isQuestion, enclosedIn ,askeds,hide,assumedTrue,assumedFalse)))
            else:
                raise Found( ("Useless "+kind+condName+"at top level" if debugMetaTemplate else "")+applyTemplate(value,isQuestion, enclosedIn ,askeds,hide,assumedTrue,assumedFalse))
        #condName is new 
        if kind=="#":
            localAssumedTrue = assumedTrue| frozenset([condName])
            localAssumedFalse = assumedFalse
        else:
            assert kind == "^"
            localAssumedFalse = assumedFalse| frozenset([condName])
            localAssumedTrue = assumedTrue
        raise Found( ("{{"+kind+condName+"}}"+("<!----- new "+kind+condName+"-->" if debugMetaTemplate else "")+applyTemplate(value, isQuestion, enclosedIn=enclosedIn,askeds=askeds,hide=hide,assumedTrue=localAssumedTrue,assumedFalse=localAssumedFalse)+"{{/"+condName+"}}"))
      except Found as found:
          #showWarning("from "+matchObject.group(0)+"\n-------------\nto\n"+found.value)
          return found.value
    return re.sub(allRegex,subFun,template,flags=flag)


def runModel(model, c=False):
    global nonExistingMeta, clean, debugMetaTemplate
    clean=c
    nonExistingMeta = set ()
    createDic(model['css'])
    debugMetaTemplate = True if re.findall(r"=debug=",model['css']) else False
    for tmpl in model['tmpls']:
        for key in ["afmt","qfmt","bafmt","bqfmt"]:
            if key in tmpl and tmpl[key]:
                tmpl[key] = applyTemplate(tmpl[key],("question" if "q" in key else "answer"))
                #ask = "Change \n"+template+"\n-----------------\nto:\n-----------------\n"+newTemplate
                #                if askUser(ask):
                # else:
                #     showWarning("meta mentionned which do(es) not exists: "+str(nonExistingMeta)+".")
                #     raise
    mm=mw.col.models
    mm.save(model)
    mm.flush()
    if nonExistingMeta and not clean:
        showWarning("meta mentionned which do(es) not exists: "+str(nonExistingMeta)+".")



def runMain(clean):
    col = mw.col
    mm = col.models
    models = mm.all()
    for model in models :
        runModel(model,clean=clean)

def runBrowser(browser, clean):
    nids=browser.selectedNotes()
    mids = set()
    for nid in nids:
        note = mw.col.getNote(nid)
        mid = note.mid
        if mid not in mids:
            mids.add(mid)
            model=mw.col.models.get(mid)
            runModel(model,clean)
    tooltip("Ending "+("cleaning " if clean else "")+"MetaTemplate")


#  #layout
# def runClayout(self):
#     "self is a clayout"
#     runModel(self.model)
#     self.redrawing=False
#     self.saveCard()
#     self.redraw()
    
# oldSetupButtons=CardLayout.setupButtons
# def newSetupButtons(self):
#     oldSetupButtons(self)
#     l=self.buttons
#     AutoTemplateField = QPushButton(_("Apply MetaTemplate"))
#     AutoTemplateField.setAutoNotAsked(False)
#     l.addWidget(AutoTemplateField)
#     AutoTemplateField.clicked.connect((lambda: runClayout(self)))
    
    
# CardLayout.setupButtons = newSetupButtons
#############################


def setupMenu(browser):
    a = QAction("MetaTemplate", browser)
    a.setShortcut(QKeySequence("Ctrl+Alt+T"))
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: runBrowser(e,False))
    browser.form.menuEdit.addAction(a)

    a = QAction("CleanTemplate", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: runBrowser(e,True))
    browser.form.menuEdit.addAction(a)

addHook("browser.setupMenus", setupMenu)

###Add buttons to main window
action = QAction(aqt.mw)
action.setText("MetaTemplate")

mw.form.menuTools.addAction(action)
action.triggered.connect(lambda: runMain(False))
action = QAction(aqt.mw)
action.setText("Clean MetaTemplate")
mw.form.menuTools.addAction(action)
action.triggered.connect(lambda: runMain(True))
