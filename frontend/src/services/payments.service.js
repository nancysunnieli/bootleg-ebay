import axios from "axios";
import { API_URL } from "../config";

const createPaymentCard = async (user_id, card_number, security_code, expiration_date) => {
    const response = await axios.post(API_URL + "payments/card", {
        user_id,
        card_number,
        security_code,
        expiration_date,
    });
    console.log("response", response);
    return response.data;
};

const getPaymentCard = async (payment_id) => {
    const response = await axios.get(API_URL + "payments/card/" + payment_id);
    console.log("response", response);
    return response.data;
};

const getPaymentCardByUserID = async (user_id) => {
    const response = await axios.get(API_URL + "payments/card_by_user/" + user_id);
    console.log("response", response);
    return response.data;
};

const paymentsDeleteAccount = async (payment_id) => {
    const response = await axios.delete(API_URL + "payments/card/" + payment_id);
    console.log("response", response);
    return response.data;
};

const createTransaction = async (user_id, payment_id, item_id, money, quantity) => {
    const response = await axios.post(API_URL + "payments/transaction", {
        user_id,
        payment_id,
        item_id,
        money,
        quantity,
    });
    console.log("response", response);
    return response.data;
};

const getTransaction = async (transaction_id) => {
    const response = await axios.get(API_URL + "payments/transaction/" + transaction_id);
    console.log("response", response);
    return response.data;
};

const getTransationsByUserId = async (user_id) => {
    const response = await axios.get(API_URL + `payments/transactions_by_user_id/${user_id}`);

    return response.data;
};

const PaymentsService = {
    createPaymentCard,
    getPaymentCard,
    getPaymentCardByUserID,
    paymentsDeleteAccount,
    createTransaction,
    getTransaction,
    getTransationsByUserId,
};

export default PaymentsService;
