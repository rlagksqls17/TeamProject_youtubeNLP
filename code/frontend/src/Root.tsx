import React from "react";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";
import {
  AboutPage,
  LoginPage,
  MainPage,
  NotFound,
  SignUpPage,
  DashBoard,
  Contents,
  Profile,
  Setting,
  Notification,
  AllFeedBackPage,
  PosFeedBackPage,
  NegFeedBackPage,
  ContentsFeedBackPage,
} from "./Pages";
import ROUTES from "./constants/routes";

const Root: React.FC = () => (
  <BrowserRouter>
    <Switch>
      <Route exact path={ROUTES.HOME} component={MainPage} />
      <Route path={ROUTES.ABOUT} component={AboutPage} />
      <Route path={ROUTES.DASHBOARD} exact component={DashBoard} />
      <Route path={ROUTES.CONTENTS} component={Contents} />
      <Route path={ROUTES.PROFILE} component={Profile} />
      <Route path={ROUTES.SETTING} component={Setting} />
      <Route path={ROUTES.NOTIFICATION} component={Notification} />
      <Route path={ROUTES.LOGIN} component={LoginPage} />
      <Route path={ROUTES.SIGNUP} component={SignUpPage} />
      <Route path={ROUTES.NOTFOUND} component={NotFound} />
      <Route path={ROUTES.ALLFEEDBACK} component={AllFeedBackPage} />
      <Route path={ROUTES.POSFEEDBACK} component={PosFeedBackPage} />
      <Route path={ROUTES.NEGFEEDBACK} component={NegFeedBackPage} />
      <Route path={ROUTES.CONTENTSFEEDBACK} component={ContentsFeedBackPage} />
      <Redirect path="*" to="/notFound" />
    </Switch>
  </BrowserRouter>
);
export default Root;
