import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
//import { AboutComponent } from './about/about.component';
//import { PrivacyComponent } from './privacy/privacy.component';
//import { TermsComponent } from './terms/terms.component';
import { DocumentComponent } from './document/document.component'
import { VerseService } from './manager.service';
import { Configuration } from './configuration';
import { HomeInterceptor } from './home/home.interceptor'

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
//import { ArticlesModule } from './articles/articles.module';
//import { ProductsModule } from './products/products.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { NgMaterialModule } from './ng-material/ng-material.module';
import { MatBasicComponent } from './ng-material/mat-basic/mat-basic.component';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { ListArticlesComponent } from './list-articles/list-articles.component';

@NgModule({
  declarations: [
    AppComponent, 
    HomeComponent,
    //AboutComponent,
    //PrivacyComponent,
    //TermsComponent,
    DocumentComponent,
    PageNotFoundComponent,
    ListArticlesComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    NgbModule,
    //ArticlesModule,
    //ProductsModule,
    AppRoutingModule,
    HttpClientModule,
    NgMaterialModule,
  ],
  entryComponents: [
    MatBasicComponent,
  ],
  providers: [
    Configuration,
    VerseService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HomeInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
}) 
export class AppModule { }
