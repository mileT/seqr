import React from 'react'
import ReactDOM from 'react-dom'
import { AppContainer } from 'react-hot-loader'

import InitialSettingsProvider from '../../shared/components/setup/InitialSettingsProvider'
import PerfProfiler from '../../shared/components/setup/PerfProfiler'
import ReduxInit from '../../shared/components/setup/ReduxInit'
import BaseLayout from '../../shared/components/BaseLayout'
import CaseReviewBreadCrumbs from './components/CaseReviewBreadCrumbs'
import CaseReviewTable from './components/CaseReviewTable'
import PedigreeZoomModal from './components/table-body/family/PedigreeZoomModal'
import EditFamilyInfoModal from './components/table-body/family/EditFamilyInfoModal'
import ViewPhenotipsModal from './components/table-body/individual/ViewPhenotipsModal'

import rootReducer, { getStateToSave, applyRestoredState } from './reducers/rootReducer'

import '../../shared/global.css'
import './casereview.css'

// render top-level component
ReactDOM.render(
  <PerfProfiler enableWhyDidYouUpdate={false} enableVisualizeRender={false}>
    <AppContainer>
      <InitialSettingsProvider>
        <ReduxInit storeName="casereview" rootReducer={rootReducer} getStateToSave={getStateToSave} applyRestoredState={applyRestoredState}>
          <BaseLayout>
            <CaseReviewBreadCrumbs />
            <CaseReviewTable />
          </BaseLayout>
          <EditFamilyInfoModal />
          <PedigreeZoomModal />
          <ViewPhenotipsModal />
        </ReduxInit>
      </InitialSettingsProvider>
    </AppContainer>
  </PerfProfiler>,
  document.getElementById('reactjs-root'),
)
