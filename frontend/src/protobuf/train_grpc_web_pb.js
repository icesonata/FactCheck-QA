/**
 * @fileoverview gRPC-Web generated client stub for 
 * @enhanceable
 * @public
 */

// GENERATED CODE -- DO NOT EDIT!


/* eslint-disable */
// @ts-nocheck



const grpc = {};
grpc.web = require('grpc-web');

const proto = require('./train_pb.js');

/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?grpc.web.ClientOptions} options
 * @constructor
 * @struct
 * @final
 */
proto.TrainClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options.format = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

};


/**
 * @param {string} hostname
 * @param {?Object} credentials
 * @param {?grpc.web.ClientOptions} options
 * @constructor
 * @struct
 * @final
 */
proto.TrainPromiseClient =
    function(hostname, credentials, options) {
  if (!options) options = {};
  options.format = 'text';

  /**
   * @private @const {!grpc.web.GrpcWebClientBase} The client
   */
  this.client_ = new grpc.web.GrpcWebClientBase(options);

  /**
   * @private @const {string} The hostname
   */
  this.hostname_ = hostname;

};


/**
 * @const
 * @type {!grpc.web.MethodDescriptor<
 *   !proto.InputData,
 *   !proto.StatusCode>}
 */
const methodDescriptor_Train_Training = new grpc.web.MethodDescriptor(
  '/Train/Training',
  grpc.web.MethodType.UNARY,
  proto.InputData,
  proto.StatusCode,
  /**
   * @param {!proto.InputData} request
   * @return {!Uint8Array}
   */
  function(request) {
    return request.serializeBinary();
  },
  proto.StatusCode.deserializeBinary
);


/**
 * @param {!proto.InputData} request The
 *     request proto
 * @param {?Object<string, string>} metadata User defined
 *     call metadata
 * @param {function(?grpc.web.RpcError, ?proto.StatusCode)}
 *     callback The callback function(error, response)
 * @return {!grpc.web.ClientReadableStream<!proto.StatusCode>|undefined}
 *     The XHR Node Readable Stream
 */
proto.TrainClient.prototype.training =
    function(request, metadata, callback) {
  return this.client_.rpcCall(this.hostname_ +
      '/Train/Training',
      request,
      metadata || {},
      methodDescriptor_Train_Training,
      callback);
};


/**
 * @param {!proto.InputData} request The
 *     request proto
 * @param {?Object<string, string>=} metadata User defined
 *     call metadata
 * @return {!Promise<!proto.StatusCode>}
 *     Promise that resolves to the response
 */
proto.TrainPromiseClient.prototype.training =
    function(request, metadata) {
  return this.client_.unaryCall(this.hostname_ +
      '/Train/Training',
      request,
      metadata || {},
      methodDescriptor_Train_Training);
};


module.exports = proto;

