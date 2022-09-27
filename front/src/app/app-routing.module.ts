import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
//import { AboutComponent } from './about/about.component';
//import { PrivacyComponent } from './privacy/privacy.component';
//import { TermsComponent } from './terms/terms.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
//import { ArticlesComponent } from './articles/documents/documents.component';
//import { ArticleDetailsComponent } from './articles/article-details/article-details.component';
import { DocumentComponent } from './document/document.component'
import { ListArticlesComponent } from './list-articles/list-articles.component'

const routes: Routes = [
  { path: 'home', component: HomeComponent },
//  { path: 'about',        component: AboutComponent },
//  { path: 'privacy',        component: PrivacyComponent },
//  { path: 'terms', component: ListArticlesComponent },
  { path: 'alldocuments', component: DocumentComponent },
  { path: 'listArticles/:doc_id', component: ListArticlesComponent },
  { path: '',   redirectTo: '/home', pathMatch: 'full' },
  { path: '**', component: PageNotFoundComponent },
//  { path: 'articles', component: ArticlesComponent, data: { animation: 'articles' } },
];

@NgModule({
  imports: [RouterModule.forRoot(
    routes,
    { enableTracing: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
