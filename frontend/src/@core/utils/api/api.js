import { SearchClient } from '@core/proto/serve_grpc_web_pb';
import { Data } from '@core/proto/serve_pb';
import { formatDataSearch } from '@core/utils/modules/modules';
import axios from 'axios';

const metadata = { 'custom-header-1': 'SearchResult' };

export const search = async (text, number) => {
  return await new Promise((resolve, reject) => {
    var client = new SearchClient('http://backend.ttst.asia');
    var req = new Data();
    req.setMessage(text);
    req.setResultNumber(number);
    try {
      client.search(req, metadata, (error, result) => {
        if (error) {
          resolve(false);
        }
        var data = [];
        var trackingData = [];
        trackingData.push({ percent: result.array[0][1] });
        if (result.array[0][2] === undefined) {
          trackingData.push({ desition: false });
        } else {
          trackingData.push({ desition: result.array[0][2] });
        }
        var contextData = formatDataSearch(result.array[0][0]);
        data.push(trackingData, contextData);
        data.push({ sentence: text });
        return resolve(data);
      });
    } catch (error) {
      reject(error);
    }
  });
};

export const searchAmp = async (input) => {
  return await axios.post('http://0.0.0.0:8888/api/search/answering/', input, { 'Content-Type': 'multipart/form-data' });
};
export const searchInference = async (input) => {
  return await axios.post('http://0.0.0.0:8888/api/search/inference/', input, { 'Content-Type': 'multipart/form-data' });
};