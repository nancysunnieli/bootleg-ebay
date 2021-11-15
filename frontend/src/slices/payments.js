import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import { toast } from "react-toastify";
import PaymentsService from "../services/payments.service";

export const createPaymentCard = createAsyncThunk(
    "payments/createPaymentCard",
    async ({ user_id, card_number, security_code, expiration_date }, thunkAPI) => {
        console.log("Creating payment card", user_id, card_number, security_code, expiration_date);
        try {
            const data = await PaymentsService.createPaymentCard(
                user_id,
                card_number,
                security_code,
                expiration_date
            );

            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const getPaymentCard = createAsyncThunk(
    "payments/getPaymentCard",
    async ({ payment_id }, thunkAPI) => {
        try {
            const data = await PaymentsService.getPaymentCard(payment_id);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const getPaymentCardByUserID = createAsyncThunk(
    "payments/getPaymentCardByUserID",
    async ({ user_id }, thunkAPI) => {
        try {
            const data = await PaymentsService.getPaymentCardByUserID(user_id);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const paymentsDeleteAccount = createAsyncThunk(
    "payments/paymentsDeleteAccount",
    async ({ payment_id }, thunkAPI) => {
        try {
            const data = await PaymentsService.paymentsDeleteAccount(payment_id);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const getTransaction = createAsyncThunk(
    "payments/getTransaction",
    async ({ transaction_id }, thunkAPI) => {
        try {
            const data = await PaymentsService.getTransaction(transaction_id);
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const createTransaction = createAsyncThunk(
    "payments/createTransaction",
    async ({ user_id, payment_id, item_id, money, quantity }, thunkAPI) => {
        try {
            const data = await PaymentsService.createTransaction(
                user_id,
                payment_id,
                item_id,
                money,
                quantity
            );
            return data;
        } catch (error) {
            const message = error.toString();
            return thunkAPI.rejectWithValue(message);
        }
    }
);

const initialState = {
    paymentCard: null,
    getPaymentCardLoading: true,
    createPaymentCardLoading: true,
    cardModalVisible: false,
};

const paymentsSlice = createSlice({
    name: "payments",
    initialState,
    reducers: {
        setCardModalVisible(state, action) {
            state.cardModalVisible = action.payload;
        },
    },
    extraReducers: {
        [createPaymentCard.pending]: (state, action) => {
            state.createPaymentCardLoading = true;
        },
        [createPaymentCard.fulfilled]: (state, action) => {
            state.createPaymentCardLoading = false;
            state.paymentCard = action.payload;
        },
        [createPaymentCard.rejected]: (state, action) => {
            state.createPaymentCardLoading = false;
            toast.error(`Oops, something went wrong ${action.payload}`);
        },
        [getPaymentCardByUserID.pending]: (state, action) => {
            console.log("F1", action.payload);
            state.getPaymentCardLoading = true;
        },
        [getPaymentCardByUserID.fulfilled]: (state, action) => {
            console.log("F", action.payload);
            state.paymentCard = action.payload;
            state.getPaymentCardLoading = false;
        },
        [getPaymentCardByUserID.rejected]: (state, action) => {
            state.getPaymentCardLoading = false;
            toast.error(`Oops, something went wrong ${action.payload}`);
        },
        [paymentsDeleteAccount.fulfilled]: (state, action) => {
            toast.success("Succesfully deleted Payment Card");
            state.paymentCard = null;
        },
    },
});

export const { setCardModalVisible } = paymentsSlice.actions;

export default paymentsSlice.reducer;
