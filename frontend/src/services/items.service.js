import axios from "axios";
import { API_URL } from "../config";

export const getUserInfo = (user_id) => {
    return axios.post(API_URL + "/Users/view_user", {
        user_id,
    });
};

export const suspendAccount = (user_id) => {
    return axios.post(API_URL + "/Users/suspend", { user_id });
};

export const modifyProfile = (user_id, fields) => {
    return axios.post(API_URL + "/Users/modify_profile", { user_id, fields });
};

export const deleteAccount = (user_id) => {
    return axios.post(API_URL + "/Users/delete_account", { user_id });
};
