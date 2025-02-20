// src/composables/useApi.js
import axios from 'axios';

export async function upload(text, if_one_time, expire_time, access_limit) {
  /*
    Upload text to server, and return a response wich contains the verify code.

    Parameters:
      text: string
      if_one_time: boolean
      expire_time: number(in seconds)
      access_limit: number
    Returns:
      res: {code: string}
      status: string
  */
  console.log(`Uploading! Params: text=${text}, if_one_time=${if_one_time}, expire_time=${expire_time}, access_limit=${access_limit}`)
  let res = null;
  let status = null;

  try {
    const response = await axios.post('/api/upload', {
      'text': text,
      'if_one_time': if_one_time,
      'expire_time': expire_time,
      'access_limit': access_limit
    })
    res = response.data
  } catch (err) {
    status = err;
  } finally {
    if (res.code === 0) {
      status = 'SUCCESS';
    }
    else {
      status = 'FAILED';
    }
  }

  console.log(`Submitted ${JSON.stringify(res)} via POST with code: ${res.data}, Status:${status}`)

  return { res, status };
}

export async function getText(code) {
  /* 
    Get text from server with verify code.

    Parameters:
      code: string
    Returns:
      res: {text: string, expire_time: number, access_limit: number}
      status: string
  */
  console.log("Getting with code: ", code)
  let res = null;
  let status = null;
  try {
    const response = await axios.get('/api/get/' + code)
    res = response.data;
  } catch (err) {
    res = err;
    status = err;
  } finally {
    if (res.code === 0) {
      status = 'SUCCESS';
    }
    else {
      status = 'FAILED';
    }
  }

  console.log(`Got ${JSON.stringify(res)} via GET with code: ${code}, Status:${status}`)
  return { res, status };

}
