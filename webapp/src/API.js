import { API } from "aws-amplify";

export default {
  getSample: async () => {
    let apiName = "ApiGatewayRestApi";
    let path = "/sample";
    const result = await API.get(apiName, path);
    // console.log('result')
    // console.log(result)
    return result;
  }

};
