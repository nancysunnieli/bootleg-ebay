import { configureStore } from "@reduxjs/toolkit";
import authReducer from "./slices/auth.js";
import itemsReducer from "./slices/items";
import profileReducer from "./slices/profile";

const reducer = {
    auth: authReducer,
    items: itemsReducer,
    profile: profileReducer,
};

const store = configureStore({
    reducer: reducer,
    devTools: true,
});

export default store;
