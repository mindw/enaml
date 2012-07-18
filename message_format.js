//-----------------------------------------------------------------------------
// Copyright (c) 2012, Enthought, Inc.
// All rights reserved.
//-----------------------------------------------------------------------------
//
//     JSON does not allow comments, so this file is marked as js.
//     However, it is describing a JSON specification
//
//-----------------------------------------------------------------------------
// Message Format
//-----------------------------------------------------------------------------
// This describes the top-level message object that is send across the
// wire between application objects. The message structure is designed
// to be flexible in the fashion the sub-parts of the message contain
// enough contextual information that they can be unpacked and passed
// directly to handler components, without the need for the handler to 
// re-parse the entire message.
//
// For applications which operate locally, they may choose to omit
// the top-level portion of the message protocol and dispatch the
// operations to their targets directly. This concession is in the
// interest of performance and practicality, and also the fact that
// local applications will typically have a single application object
// which handles routing, and the top-level data is not needed.
{
  // The id of the application instance for the message. This should
  // be unique among all other instances currently in use.
  "application_id": "<string>",

  // The id of the client which is sending/receiving the message. This
  // should be unique among all other clients currently in use.
  "client_id": "<string>",

  // The metadata supplied by the implementations. There is formally
  // no requirement for what must be placed in this object. It is 
  // entirely implementation defined and may be null.
  "metadata": null,

  // The array of operations to execute by the peer. The operations
  // must be executed in order.
  "operations": [
    {
      // The type of the operation. Will always be one of "message", 
      // "request", "response".
      "type": "<message | request | reply>",
      
      // The target of the operation is the identifier of the handler 
      // on the peer that should process the operation. These 
      // identifiers are unique and implementation depenent. They are 
      // generated as peers are created.
      "target_id": "<string>",
        
      // An identifier which uniquely defines this operation. For
      // operations of type "message", this will be null. For 
      // "request" and "reply" this will be a string which identifies
      // a "request"/"reply" pair, and can be used by an application
      // to route the operation to the proper handler.
      "operation_id": null,

      // The payload of an operation is the information required by
      // the target handler to process the operation. The payload
      // contents are partially dependent on the type of the 
      // operation.
      "payload": {
        // The action associate with this operation. The available
        // actions for a peer are dependent on the type of that
        // peer and the type of the operation. See the specification 
        // for actions for further info. (this spec is not yet defined)
        "action": "<string>",

        // The remaining properties of the payload depend on the 
        // action. See the specification for actions for further 
        // info. (this spec is not yet defined)

      }
    }
  ]
}
