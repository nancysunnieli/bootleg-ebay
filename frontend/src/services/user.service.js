import axios from "axios";
import { API_URL } from "../config";
import AuthService from "./auth.service";

export const getUserInfo = (user_id) => {
    return axios.post(API_URL + "/Users/ViewUser", {
        user_id,
    });
};

export const suspendAccount = (user_id) => {
    return axios.post(API_URL + "/Users/SuspendAccount", { user_id });
};

export const modifyProfile = (user_id, fields) => {
    return axios.post(API_URL + "/Users/ModifyProfile", { user_id, ...fields });
};

export const deleteAccount = async (user_id) => {
    const response = await axios.post(API_URL + "Users/DeleteAccount", {
        user_id,
    });
    AuthService.logout();
    return response.data;
};
