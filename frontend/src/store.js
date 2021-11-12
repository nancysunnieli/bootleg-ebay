import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./slices/auth.js";
import itemsReducer from "./slices/items";
import profileReducer from "./slices/profile";
import auctionsReducer from "./slices/auctions";
import cartReducer from "./slices/cart";

const reducer = {
    auth: authReducer,
    items: itemsReducer,
    profile: profileReducer,
    auctions: auctionsReducer,
    cart: cartReducer,
};

const store = configureStore({
    reducer: reducer,
    devTools: true,
});

export default store;
