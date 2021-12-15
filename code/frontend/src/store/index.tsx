import logger from "redux-logger";
import { configureStore } from "@reduxjs/toolkit";
import { persistStore } from "redux-persist";
import persistedReducer, { rootSaga } from "./modules";
import createSagaMiddleware from "redux-saga";

const sagaMiddleware = createSagaMiddleware();

const store = configureStore({ reducer: persistedReducer, middleware: [logger, sagaMiddleware] });

sagaMiddleware.run(rootSaga);

export type AppDispatch = typeof store.dispatch;
export const persistor = persistStore(store);
export default store;
