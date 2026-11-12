import { createRouter, createWebHistory } from "vue-router";
import { getToken } from "../api/client";
import AppShell from "../layouts/AppShell.vue";
import AnalysesPage from "../pages/AnalysesPage.vue";
import DatasetsPage from "../pages/DatasetsPage.vue";
import GovernancePage from "../pages/GovernancePage.vue";
import LoginPage from "../pages/LoginPage.vue";
import OverviewPage from "../pages/OverviewPage.vue";
import RunDetailPage from "../pages/RunDetailPage.vue";
const router=createRouter({history:createWebHistory(),routes:[
 {path:"/login",component:LoginPage},
 {path:"/",component:AppShell,children:[
  {path:"overview",component:OverviewPage},{path:"datasets",component:DatasetsPage},
  {path:"analyses",component:AnalysesPage},{path:"runs/:runId",component:RunDetailPage},
  {path:"governance",component:GovernancePage}
 ]},
 {path:"/:pathMatch(.*)*",redirect:"/overview"}
]});
router.beforeEach((to)=>{if(to.path!=="/login"&&!getToken())return "/login";if(to.path==="/login"&&getToken())return "/overview";return true});
export default router;
