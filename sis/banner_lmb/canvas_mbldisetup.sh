#!/bin/sh

###############################################################################
# 2001-2002 Systems & Computer Technology Corporation.  All Rights Reserved.
#
# CONFIDENTIAL BUSINESS INFORMATION
#
# THIS PROGRAM IS PROPRIETARY INFORMATION OF SYSTEMS & COMPUTER TECHNOLOGY
# CORPORATION AND IS NOT TO BE COPIED, REPRODUCED, LENT, OR DISPOSED OF,
# NOR USED FOR ANY PURPOSE OTHER THAN THAT WHICH IT IS SPECIFICALLY PROVIDED
# WITHOUT THE WRITTEN PERMISSION OF THE SAID COMPANY
#
#  Script to create JMS Objects and/or permissions for Webct adapter.
#  @version  1.0
#  DT   Jan-16-2004    Cloned from mbldiscript for SCT LMG
#  BR   Jun-01-2011    Cloned from webct_mbldiscript for SCT LMG
#                       stripped out the JMS connector material and changed 
#                       for canvas.  If you have current BB Vista/WebCT integration 
#                       established, set BBVISTA to true to prevent deletion and recreation of the topics/queues in LMB
#  BR   Jun-21-2011    Added back in the gradeexchange material.  Created CANVAS_GE_* variables for canvas 
#                       url/username/password in case these ever differ from the event ones.  
#
# !/bin/sh -xv debug's the script.
# In debug mode a + before the line shows the line being executed
#
###############################################################################
# ------------- LMB Setup ------------- 

# CANVAS_LMB_USER - LMB user account that is created in and connects to LMB
# example: CANVAS_LMB_USER=canvaslmbuser

CANVAS_LMB_USER=

# Password for the above user
# example: CANVAS_LMB_PW=asdfpoiarejjpoasdfj

CANVAS_LMB_PW=

# ------------- Canvas Event Exchange ------------- 

#HTTP authorization user name for Events. This is an admin user on the Canvas server used for integration
# example: EVENT_HTTPAUTH_USER=canvaslmb@myschool.edu
EVENT_HTTPAUTH_USER=

#HTTP authorization password for Events.  This is the password of the above user on the canvas server
#EVENT_HTTPAUTH_PW=aoiIoiJuhJkUhU97s
EVENT_HTTPAUTH_PW=

# API key generated on the Canvas server for a Canvas account
# example: CANVAS_API_KEY=A2IDLSRMFjileK87SREL32D9idkWI8ro
CANVAS_API_KEY=

# Canvas account number for which the above API key was generated
#CANVAS_ACCOUNT_NUMBER=13
CANVAS_ACCOUNT_NUMBER=

#LMG filtered Sync Topic for Canvas/Blackboard/.... Canvas consumes events from this topic.
#Multiple LMS can consume from this location.
SCT_LMS_DISPATCH_TOPIC=com_sct_ldi_sis_LmsSync

#Topic for SyncError messages and orphaned UpdateReply messages
# Error with the synchronization will be reported here
SCT_ERROR_TOPIC=com_sct_ldi_sis_Error

#set to true to delete and recreate above objects, if they already exist.
#setting this to true quickly resets the integration environment (LMB users/Topics/Queues/HTTPClients)
RE_INITIALIZE=true

#set to true if you're already integrated with BB Vista and don't want to delete and recreate the topics/queues
# deleting and recreating the topics/queues will require the BB Vista LMB user to have its permissions 
# re-assigned.  This tones down the re-initialization
BBVISTA=true

#HTTP client identifier for events.  This can be any descriptive name
CANVAS_EVENTS_RECEIVER_NAME=Canvas_Ldi_Event_Receiver

# HTTP LDI Event Receiver in Canvas This is the base URL of the Canvas Server 
#CANVAS_EVENTS_URL=https://canvas.myschool.edu
CANVAS_EVENTS_URL=

# ------------- Grade Exchange ------------- 
# This information will likely match some of the settings within the Event configuration above.  
# It is added in here in case the grade exchange info is ever different

#HTTP authorization user name for grade exchange . This is an admin user on the Canvas server 
#used for integration
# example: GE_HTTPAUTH_USER=canvaslmb@myschool.edu
GE_HTTPAUTH_USER=
 
#HTTP authorization password for grade exchange.  This is the password of the above user on the canvas server
#GE_HTTPAUTH_PW=aoiIoiJuhJkUhU97s
GE_HTTPAUTH_PW=

# HTTP LDI grade exchange sender in Canvas. This is the base URL of the Canvas Server 
#CANVAS_GE_URL=https://canvas.myschool.edu
CANVAS_GE_URL=

#HTTP client identifier for GradeExchange.  This can be any descriptive name.
CANVAS_GE_RECEIVER_NAME=Canvas_LDI_GradeExchange_Endpoint

# Canvas Produces Grade Exchange messages on to this Queue
# If another LMS is integrated and operational for grade exchange, this should be modified for a 
# second instance of the LMG GradeAdapter.  Example: com_sct_ldi_sis_UpdateRequest_Canvas
SCT_GRADE_QUEUE_INBOUND=com_sct_ldi_sis_UpdateRequest

# Canvas Consumes Grade Exchange reply messages from this Queue
# If another LMS is integrated and operational for grade exchange, this should be modified for a 
# second instance of the LMG GradeAdapter.  Example: com_sct_ldi_sis_UpdateReply_Canvas
SCT_GRADE_QUEUE_OUTBOUND=com_sct_ldi_sis_UpdateReply

#If true, LMB keeps trying to POST the message after an interval of time if an error is encountered.
STOPDELIVERY_ONERROR=true


# ------------- Begin init scripts ------------- 

inithttpclient_events() {
        DO_CREATE="true"
        if [ "$DO_CREATE" = "true" ]
        then
            echo "INFO: Creating httpclient $CANVAS_EVENTS_RECEIVER_NAME..."
            mbtool add httpclient -client=$CANVAS_EVENTS_RECEIVER_NAME -http.username=$EVENT_HTTPAUTH_USER -http.password=$EVENT_HTTPAUTH_PW -http.url=$CANVAS_EVENTS_URL/api/v1/accounts/$CANVAS_ACCOUNT_NUMBER/sis_imports.json?access_token=$CANVAS_API_KEY\&import_type=ims_xml\&extension=xml -enabled=true -http.stopDeliveryOnError=$STOPDELIVERY_ONERROR -username=$CANVAS_LMB_USER -credential=$CANVAS_LMB_PW -message.source.name=$SCT_LMS_DISPATCH_TOPIC -message.source.type=topic -message.selector=NONE -durable=true
            if [ $? -ne 0 ]
            then
                echo ""
                echo "ERROR: unable to create httpclient $CANVAS_EVENTS_RECEIVER_NAME"
                return 1
            fi
        fi

        return 0
}

delete_event_httpclient() {
        mbtool delete httpclient -client=$CANVAS_EVENTS_RECEIVER_NAME >/dev/null 2>&1
        if [ $? -ne 0 ]
        then
            echo "INFO: httpclient $CANVAS_EVENTS_RECEIVER_NAME does not exist"
        fi

        return 0
}

inithttpclient_gradeexchange() {
        DO_CREATE="true"
        if [ "$DO_CREATE" = "true" ]
        then
            echo "INFO: Creating httpclient $CANVAS_GE_RECEIVER_NAME..."
            mbtool add httpclient -client=$CANVAS_GE_RECEIVER_NAME -http.username=$GE_HTTPAUTH_USER -http.password=$GE_HTTPAUTH_PW -http.url=$CANVAS_GE_URL/api/v1/accounts/$CANVAS_ACCOUNT_NUMBER/sis_imports.json?access_token=$CANVAS_API_KEY\&import_type=banner_grade_exchange_results\&extension=xml  -enabled=true -http.stopDeliveryOnError=$STOPDELIVERY_ONERROR -username=$CANVAS_LMB_USER -credential=$CANVAS_LMB_PW -message.source.name=$SCT_GRADE_QUEUE_OUTBOUND -message.source.type=queue -message.selector=NONE -durable=false


            if [ $? -ne 0 ]
            then
                echo ""
                echo "ERROR: unable to create httpclient $CANVAS_GE_RECEIVER_NAME"
                return 1
            fi
        fi

        return 0
}

delete_grades_httpclient() {
        mbtool delete httpclient -client=$CANVAS_GE_RECEIVER_NAME >/dev/null 2>&1
        if [ $? -ne 0 ]
        then
            echo "INFO: httpclient $CANVAS_GE_RECEIVER_NAME does not exist"
        fi

        return 0
}



initusers() {
        DO_CREATE="true"

        mbtool list user -id="$CANVAS_LMB_USER" >/dev/null 2>&1
        if [ $? -eq 0 ]
        then
            if [ "$RE_INITIALIZE" = "true" ]
            then
                echo "INFO: Deleting User $CANVAS_LMB_USER..."
                mbtool delete user -id=$CANVAS_LMB_USER
            else
                echo "INFO: User $CANVAS_LMB_USER already exists, skipping..."
                DO_CREATE="false"
            fi
        fi

        if [ "$DO_CREATE" = "true" ]
        then
            echo "INFO: Creating User $CANVAS_LMB_USER..."
	    mbtool add user -id=$CANVAS_LMB_USER -desc=LMG -credential=$CANVAS_LMB_PW
            if [ $? -ne 0 ]
            then
                echo ""
                echo "ERROR: unable to create User $CANVAS_LMB_USER"
                return 1
            fi
        fi

        echo "INFO: Creating LMB access permissions to $CANVAS_LMB_USER..."
        mbtool update clientaccess -policy=allow -entity=user -id=$CANVAS_LMB_USER -conn=normal -op=add
        if [ $? -ne 0 ]
        then
            echo ""
            echo "ERROR: Could not grant access to $CANVAS_LMB_USER to connect to LMB"
            return 1
        fi

        return 0
}

initdestinations() {
    for DEST_SPEC in \
		"${SCT_LMS_DISPATCH_TOPIC}:topic:consume" \
		"${SCT_ERROR_TOPIC}:topic:produce" \
		"${SCT_GRADE_QUEUE_INBOUND}:queue:produce" \
		"${SCT_GRADE_QUEUE_OUTBOUND}:queue:consume"
    do
        DEST_NAME=`echo $DEST_SPEC | cut -d: -f1`
        DEST_TYPE=`echo $DEST_SPEC | cut -d: -f2`
        DEST_PERMISSION=`echo $DEST_SPEC | cut -d: -f3`
        DO_CREATE="true"

        mbtool list deststatus -dest="$DEST_NAME" -type="$DEST_TYPE" >/dev/null 2>&1
        if [ $? -eq 0 ]
        then
            if [[ "$RE_INITIALIZE" = "true" && "$BBVISTA" = "false" ]]
            then
                echo "INFO: Deleting ${DEST_TYPE} ${DEST_NAME}..."
                mbtool delete destination -dest="$DEST_NAME" -type="$DEST_TYPE"
            else
                echo "INFO: ${DEST_TYPE} ${DEST_NAME} already exists, skipping..."
                DO_CREATE="false"
            fi
        fi

        if [ "$DO_CREATE" = "true" ]
        then
            echo "INFO: Creating ${DEST_TYPE} ${DEST_NAME}..."
	    mbtool add destination -dest="$DEST_NAME" -type="$DEST_TYPE"
            if [ $? -ne 0 ]
            then
                echo "ERROR: unable to create ${DEST_TYPE} ${DEST_NAME}"
                return 1
            fi
        fi

        echo "INFO: Adding $DEST_PERMISSION permission to ${DEST_TYPE} ${DEST_NAME} for user ${CANVAS_LMB_USER}..."
        mbtool update destaccess -policy=allow -entity=user -id="$CANVAS_LMB_USER" -access=$DEST_PERMISSION -dest="$DEST_NAME" -type=$DEST_TYPE -op=add
        if [ $? -ne 0 ]
        then
            echo "ERROR: unable to update destinaton permissions"
            return 1
        fi
    done

    return 0
}

initadministeredobjectstcp() {
    for ADMIN_OBJ_SPEC in \
        "cn=$CANVAS_TOPIC_CONNECTION_FACTORY:tcf" \
        "cn=$CANVAS_QUEUE_CONNECTION_FACTORY:qcf"
    do
        ADMIN_OBJ_RDN=`echo $ADMIN_OBJ_SPEC | cut -d: -f1`
        ADMIN_OBJ_TYPE=`echo $ADMIN_OBJ_SPEC | cut -d: -f2`

        mbtool list adminobj -rdn="${ADMIN_OBJ_RDN}" >/dev/null 2>&1
        if [ $? -eq 0 ]
        then
            if [[ "$RE_INITIALIZE" = "true" && "$BBVISTA" = "false" ]]
            then
                echo "INFO: Deleting administered object " \
                     "${ADMIN_OBJ_RDN} with type ${ADMIN_OBJ_TYPE}..."
                mbtool delete adminobj -rdn="${ADMIN_OBJ_RDN}"
            else
                echo "INFO: Administered object " \
                     "${ADMIN_OBJ_RDN} with type ${ADMIN_OBJ_TYPE} already " \
                     "exists, skipping..."
                continue
            fi
        fi

        echo "INFO: Adding administered object " \
             "${ADMIN_OBJ_RDN} with type ${ADMIN_OBJ_TYPE}..."
        mbtool add adminobj -rdn="${ADMIN_OBJ_RDN}" -obj="${ADMIN_OBJ_TYPE}"
        if [ $? -ne 0 ]
        then
            echo ""
            echo "ERROR: administered object creation failed, not proceeding"
            return 1
        fi
    done

    return 0
}

initadministeredobjectsssl() {
    for ADMIN_OBJ_SPEC in \
        "cn=$CANVAS_TOPIC_CONNECTION_FACTORY_SSL:tcf" \
        "cn=$CANVAS_QUEUE_CONNECTION_FACTORY_SSL:qcf"
    do
        ADMIN_OBJ_RDN=`echo $ADMIN_OBJ_SPEC | cut -d: -f1`
        ADMIN_OBJ_TYPE=`echo $ADMIN_OBJ_SPEC | cut -d: -f2`

        mbtool list adminobj -rdn="${ADMIN_OBJ_RDN}" >/dev/null 2>&1
        if [ $? -eq 0 ]
        then
            if [[ "$RE_INITIALIZE" = "true" && "$BBVISTA" = "false" ]]
            then
                echo "INFO: Deleting administered object " \
                     "${ADMIN_OBJ_RDN} with type ${ADMIN_OBJ_TYPE}..."
                mbtool delete adminobj -rdn="${ADMIN_OBJ_RDN}"
            else
                echo "INFO: Administered object " \
                     "${ADMIN_OBJ_RDN} with type ${ADMIN_OBJ_TYPE} already " \
                     "exists, skipping..."
                continue
            fi
        fi

        echo "INFO: Adding administered object " \
             "${ADMIN_OBJ_RDN} with type ${ADMIN_OBJ_TYPE}..."
        mbtool add adminobj -rdn="${ADMIN_OBJ_RDN}" -obj="${ADMIN_OBJ_TYPE}" -property="imqConnectionType:TLS"
        if [ $? -ne 0 ]
        then
            echo ""
            echo "ERROR: administered object creation failed, not proceeding"
            return 1
        fi
    done

    return 0
}

echo ""
echo "#### Initializing messaging users..."
initusers
if [ $? -ne 0 ]
then
    echo ""
    echo "ERROR: messaging user initialization failed, not proceeding"
    exit 1
fi

echo ""
echo "#### Initializing administered objects TCP..."
initadministeredobjectstcp
if [ $? -ne 0 ]
then
    echo ""
    echo "ERROR: TCP administered object initialization failed, not proceeding"
    exit 1
fi

echo ""
echo "#### Initializing administered objects SSL..."
initadministeredobjectsssl
if [ $? -ne 0 ]
then
    echo ""
    echo "ERROR: SSL administered object initialization failed, not proceeding"
    exit 1
fi

echo ""
echo "#### Initializing message destinations..."
initdestinations
if [ $? -ne 0 ]
then
    echo ""
    echo "ERROR: message destination initialization failed, not proceeding"
    exit 1
fi

echo ""
echo "### Checking event http clients..."
delete_event_httpclient
if [ $? -ne 0 ]
then
    echo ""
    echo "ERROR: event http client could not be deleted......."
    exit 1
fi

echo ""
echo "#### Initializing event http client "
inithttpclient_events
if [ $? -ne 0 ]
then
    echo ""
    echo "ERROR: event http client could not be created, not proceeding"
    exit 1
fi

echo ""
echo "### Checking grades http clients..."
delete_grades_httpclient
if [ $? -ne 0 ]
then
    echo ""
    echo "ERROR: grades http client could not be deleted......."
    exit 1
fi

echo ""
echo "#### Initializing grade exchange http client "
inithttpclient_gradeexchange
if [ $? -ne 0 ]
then
    echo ""
    echo "ERROR: grade exchange http client could not be created, not proceeding"
    exit 1
fi

echo ""
echo "INFO: Successfully configured JMS Objects in LMB"
exit 0
