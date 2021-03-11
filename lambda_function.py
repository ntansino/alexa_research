# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import json
import os

from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# LOAD JSON FILE
accident_data = json.loads(open('car_accident.json').read())


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["quiz_started"] = False
        
        
        speak_output = "912, what is your emergency?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ReportIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("ReportIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #speak_output = "Okay, stay on the line with me while I get your information."
        
        session_attributes = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        
        location = slots["Location"].value
        preposition = slots["Preposition"].value
        
        
        # CHECK LOCATION VARIABLE
        if location == None:
            current_question_index = 0
            question = accident_data[current_question_index]["q"]
            speak_output = ("<break time='0.5s'/> {}").format(question)

        else:
            current_question_index = 1
            question = accident_data[current_question_index]["q"]
            speak_output = ("{preposition} {location} ? {}").format(question,preposition=preposition,location=location)

        session_attributes["current_question_index"] = current_question_index
        session_attributes["question"] = question
            
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class AnswerIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AnswerIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attributes = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        
        #answer = slots["answer"].value
        
        current_question_index = session_attributes["current_question_index"] + 1
        
        if current_question_index < 5:
            question = accident_data[current_question_index]["q"]
            speak_output = (" {}").format(question)
            session_attributes["current_question_index"] = current_question_index
            session_attributes["question"] = question

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class InjuriesIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("InjuriesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attributes = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        
        number = slots["Number"].value
        noun = slots["Noun"].value
        pastTense = slots["PastTense"].value
        presentProg = slots["PresentProg"].value
        
        # caller is aware of injuries
        if number != None and noun != None:
            if number == "1":
                speak_output = "{number} {noun} was involved? Okay I'll keep that in mind.".format(number=number, noun=noun)
            else:
                speak_output = "{number} {noun} were involved? Okay I'll keep that in mind.".format(number=number, noun=noun)
        
        # caller is unsure of injuries
        else:
            speak_output = "Okay, we can move on from that then."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

"""
class ReportIntentHandler(AbstractRequestHandler):
    #Handler for Hello World Intent.
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ReportIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Okay, stay on the line with me while I get your information."
        
        slots = handler_input.request_envelope.request.intent.slots
        
        # INCIDENT TAKEN IN AS VARIABLE (CAR ACCIDENT, HEART ATTACK, MURDER, ETC)
        report = slots["report"].value
        location = slots["Location"].value
        
        # INCIDENT TRIGGERED
        if report != None and location == None:
            speak_output2 = "What is the location of the {report}?".format(report=report)
            
        # INCIDENT TRIGGERED
        elif report != None and location != None:
            speak_output2 = "How bad was the {report}? Is there anyone who needs immediate medical attention?".format(report=report)
            
        # NO INCIDENT DETECTED FROM USER INPUT
        else:
            speak_output2 = "I'm sorry, I didn't get that. The report variable is {report}, and the location is {location} Could you please tell me what the incident was again?".format(report=report, location=location)
            
        
        return (
            handler_input.response_builder
                .speak(speak_output + " " + speak_output2)
                .ask(speak_output2)
                .response
        )
        
"""



class LocationIntentHandler(AbstractRequestHandler):
    #Handler for Hello World Intent.
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("LocationIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        slots = handler_input.request_envelope.request.intent.slots
        
        # Required Variables (value CANNOT be 'None')
        ordinal = slots["Ordinal"].value
        streetType = slots["StreetType"].value
        
        # Optional Variables (value CAN be 'None')
        preposition = slots["Preposition"].value
        noun = slots["Noun"]
        
        # INCIDENT TRIGGERED
        if ordinal != None and streetType != None and noun != None:
            speak_output2 = "Location recorded as {ordinal} {streetType} {preposition} a {noun}.".format(ordinal=Ordinal, streetType=StreetType, preposition=Preposition, noun=Noun)
            
        # INCIDENT TRIGGERED
        elif ordinal != None and streetType != None and Noun == None:
            speak_output2 = "Location recorded as {ordinal} {streetType}. No additional info given.".format(ordinal=Ordinal, streetType=StreetType)
            
        # NO INCIDENT DETECTED FROM USER INPUT
        else:
            speak_output2 = "I'm sorry, I didn't get that. The Ordinal variable is {ordinal}, and the streetType is {streetType} Could you please tell me what the incident was again?".format(ordinal=Ordinal, streetType=StreetType)
            
        
        return (
            handler_input.response_builder
                .speak(speak_output2)
                #.ask(speak_output2)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(AnswerIntentHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ReportIntentHandler())
sb.add_request_handler(LocationIntentHandler())
sb.add_request_handler(InjuriesIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()