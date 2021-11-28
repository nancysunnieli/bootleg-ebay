import axios from "axios";
import { API_URL } from "../config";
import AuthService from "./auth.service";

export const getUserInfo = async (user_id) => {
    const response = await axios.get(API_URL + `users/user/${user_id}`);
    return response.data;
};

const suspendAccount = async (user_id) => {
    const response = await axios.put(API_URL + "users/suspend", { user_id });
    return response.data;
};

const unsuspendAccount = async (user_id) => {
    const response = await axios.put(API_URL + "users/unsuspend", { user_id });
    return response.data;
};

const modifyProfile = async (user_id, fields) => {
    const response = await axios.put(API_URL + `users/user/${user_id}`, { ...fields });
    localStorage.setItem("user", JSON.stringify(response.data));
    return response.data;
};

const deleteAccount = async (user_id) => {
    const response = await axios.delete(API_URL + `users/user/${user_id}`, { data: {} });
    AuthService.logout();
    return response.data;
};

const UserService = {
    getUserInfo,
    suspendAccount,
    unsuspendAccount,
    modifyProfile,
    deleteAccount,
};

export default UserService;
