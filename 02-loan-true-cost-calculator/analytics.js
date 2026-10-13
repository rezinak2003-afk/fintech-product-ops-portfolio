(function(){
  let enabled=false, loaded=false;
  const cfg=window.APP_CONFIG||{};
  function validId(){return /^G-[A-Z0-9]+$/.test(cfg.gaMeasurementId||'')}
  function load(){if(loaded||!validId())return;loaded=true;window.dataLayer=window.dataLayer||[];window.gtag=function(){window.dataLayer.push(arguments)};window.gtag('js',new Date());window.gtag('config',cfg.gaMeasurementId);const s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(cfg.gaMeasurementId);document.head.appendChild(s)}
  try{enabled=localStorage.getItem('analytics-consent')==='yes'}catch(e){}
  if(enabled)load();
  window.portfolioAnalytics={
    enabled:()=>enabled,
    consent:function(value){enabled=!!value;try{localStorage.setItem('analytics-consent',enabled?'yes':'no')}catch(e){};if(enabled)load();else if(validId()&&loaded){/* GA cannot be fully unloaded in this page session; reload after revocation. */}return enabled},
    track:function(name){if(enabled&&validId()&&typeof window.gtag==='function'){window.gtag('event',name,{project:'loan_true_cost_calculator'})}}
  };
})();
