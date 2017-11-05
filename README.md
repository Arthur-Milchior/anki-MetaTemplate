Copyright: Arthur Milchior arthur@milchior.fr   
License: GNU GPL, version 3 or later; [http://www.gnu.org/copyleft/gpl.html](http://www.gnu.org/copyleft/gpl.html)

Feel free to contribute to this code on [GitHub](https://github.com/Arthur-Milchior/anki-MetaTemplate)  
Anki add-on number: [172450233](https://ankiweb.net/shared/info/172450233)


A Meta Template for card's type (aka blueprient, templates)


**WARNING: NEVER check for empty cards until you did apply metaTemplate to every note type where you want to use it. Otherwise, you risk to delete cards which are not supposed to be empty, but which are because the {{tags}} does not appear in the front of cards.**

**In general, do a backup of your data BEFORE trying this addon, if either the add-on or you made a mistake, it would avoid data loss.**

### Usage 

I did realize that, given a note type, all of its card type are really similar. And usually, if I want to do an edition, I want to do it to (almost) every card types.  
Instead of doing copy-paste each time I want to do a small edit to each card's type, I created this add-on to edit multiple card's type at once.

I first give examples, I'll give the complete formal explanation below.

## Basic usage

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

Note that, if you have made change between `<span MT="var">` and `</span MT="var">`, this change has now been lost. Always do your edit either in the CSS part, or in the part which is not enclosed by MetaTemplate's tag.

you can also use edit>clean metaTemplate to have

    <span MT="var"/>
back.

(This option allows to remove the part copied from CSS to front/back. It helps to edit, review your code.)

## Recursive usage

Now add to the css:  

    /*[[var||{{#definition}}<span MT="foo" />{{/definition}}]]*/
    /*[[foo||{{definition}}]]*/
(note that  

    /*[[var||{{#definition}}<span MT="foo" />{{/definition}}]]
    [[foo||{{definition}}]]*/  
is also valid. In fact, you need just `/*` and `*/` to enclose your definition. This part means that it is code which is not really css. `/*` and `*/` will now be avoided in future examples.)

and add to some card's type front/back:
  
    <span MT="var" />
**Apply MetaTemplate.**  

    <span MT="var" />
is replaced by  

    {{#definition}}<span MT="foo" />{{/definition}}
which itself is replaced by  

    {{#definition}}{{definition}}{{/definition}}`

This is not very useful by itself, but becomes important using the following option

## Asking a part of the template

Now add to the css:  

    /*[[var||{{#definition}}<span MT="foo" />{{/definition}}]]*/
    /*[[foo||{{definition}}||Definition ?]]*/

<!--linebreak-->

    <span MT="var" />
is still replaced by 
 
    {{#definition}}{{definition}}{{/definition}}`

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


As you can see, `<span MT="foo" />` is replaced by the third element, and not the second one. This is because a metaTemplate called before stated that "foo" is "asked".  
I.e. the first element is the name of the field, the second element is its default value. The third is the question to ask instead of the important information.

## Prefix/suffix

In the previous example: var is used to enclose foo between `{{#definition}}` and `{{/definition}}`. Instead, there is an easier way, just do:
 
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

## CSS classes

    [[def||{{#definition}}||Definition: <<{{definition}}>>||<<Definition ?>>||{{/definition}}]]

Here `<<>>` is replaced by an enclosing span with classes:  

    -def  
Furthermore, in "def" occured in an "asked" field in a metatemplate which led to a call of def, then the classes are also:

    -asked
    -asked_def

Adding def is just a matter of writing quickly something I do use often.
Adding asked allows me to use a css class on elements which are asked. And more precisely, to add it on the important part of those elements. Here, it is not usefull to add it to "Definition:" since the definition is the important part.
asked_def allows me to have a class which is applied only on asked elements and which differs according to the meta template.

Note that `<<` and `>>` may also occurs in prefix and suffix. 

    [[def||{{#definition}}<<||Definition: {{definition}}||Definition ?||>>{{/definition}}]]
would be perfectly valid if you want the classes to be applied to "Definition:" too.

## Adding CSS style in MetaTemplate

If you want to add `<style>foo</style>` in a metaTemplate, use `<css>foo</css>` instead. In the card's type `<css>` tag will be replaced by `<style>` tag

## Hiding

Sometime, one may wish to state in a metaTemplate A that, another metaTemplate B, .., Z should not be shown, contrary to what happens normally when A is called. One should add the field hide="B-...-Z", as in `<span MT="foo" hide="B-C"/>`.

## Conditional mustaches

If you have conditional mustaches (i.e. `{{#foo}}{{/foo}}` or `{{^foo}}{{/foo}}`) inside a meta template, and that this template is called inside another conditional mustache, the inner conditional mustache is removed. If both conditions are similar, the content is preserved. Otherwise if the conditionals are contradictory (i.e. `{{#foo}}{{^foo}}content{{/foo}}{{/foo}})` then the content is also removed. This allow to avoid error message by anki. 

## Debugging

If, as me, you use metaTemplate a lot, you will certainly have bugs, codes which is not exactly as you want it. 
To debug it, you can  `=debug=` to your css. In this case, span metatemplate remains even when they are useless (i.e. when they occur from the application of another metatemplate), and you'll have html comment stating which conditional mustaches are contradictory/redundant. And, in each application, which field of the entry is used (i.e. prefix, default, question_asked, suffix..., see below for the full list of possibility.)

You should compile without this option before synchronizing. This option may create really huge card's type. In particular, I created cards so big that ankidroid could not handle it.

## More controls

After `||`, you may add `=fieldName=`, to state that the content is not the usual one.  
For example `[[page||=question=||=answer=Page {{page}}]]` allows you to state that a "page" meta template must be removed in question side, and is Page `{{page}}` in the answer side. I use this since knowing the page from which a note comes may be really useful to check in my books, if I fear the note have a mistake. But I don't want to see it on the question side since it my gives a hint about the kind of answer one may expect.

Note that in this case `=question=` or `=default=` is mandatory, because MetaTemplate must know which value to use on the question side.

The possible values are:

* =prefix=, =suffix=: self described
* =default=, what should be used assuming there is nothing more precise
* =question= what should be shown on question side
* =answer= what should be shown on answer side
* =asked= what should be shown if the current MetaTemplate's name is asked (i.e. belong to an "asked" field in an enclosing meta template)
* =notAsked= what should be shown if the current MetaTemplate's name is NOT asked
* =asked_question= what should be shown in the QUESTION side, when the current metaTemplate is asked
* =asked_answer= what should be shown in the ANSWER side, when the current metaTemplate is asked
* =notAsked_question= what should be shown in the QUESTION side, when the current metaTemplate is NOT asked
* =notAsked_answer= what should be shown in the ANSWER side, when the current metaTemplate is NOT asked

In the case where many entry may apply, isAsked_isQuestion/Answer has the priority. isAsked is used if the previous one is not defined, then isQuestion/Answer, and finally default. Here "isAsked" represents either "asked" or "notAsked" and isQuestion/Answer  represents "answer" or "question".

## Technical note

As always, a few problem may arise when the HTML is not valid.  
In order to accept template with unbalanced tag, I choosed the following compromise. The tag ending a `<span MetaTemplate='name'>` is the first `</span MetaTemplate='name'>`. This should cause no problem since a template should not be called inside itself. And it avoids to consider balancing of tags.

XML is not respected here. MetaTemplate should appear directly after the word span, otherwise it is not recognized. Some spaces are tolerated, but this tolerance may potentially disappear during an update. The span tag was used in order to ensure that the tag as no effect when considered in the html viewer.