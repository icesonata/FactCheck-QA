import React from 'react';
import Header from '@core/layout/header/header';
import Footer from '@core/layout/footer/footer';

export default function Layout(props) {
  return (
    <div>
      <Header />
      {props.children}
      <Footer />
    </div>
  );
}
