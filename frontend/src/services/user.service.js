import axios from "axios";
import authHeader from "./auth-header";
import { API_URL } from "../config";

const getUserInfo = (user_id) => {
  return axios.post(API_URL + "/Users/ViewUser", {
    user_id,
  });
};

export default {
  getUserInfo,
};
