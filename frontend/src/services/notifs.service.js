import axios from "axios";
import { API_URL } from "../config";

const getInbox = async () => {
    const response = await axios.get(API_URL + "notifs/inbox");
    console.log("response", response);
    return response.data;
};

const sendEmail = async (recipient, subject, body) => {
    const response = await axios.post(API_URL + "notifs/email", {
        recipient,
        subject,
        body,
    });
    return response.data;
};

const NotifsService = {
    getInbox,
    sendEmail,
};

export default NotifsService;
