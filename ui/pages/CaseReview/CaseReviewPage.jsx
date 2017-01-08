import React from 'react'
import ReactDOM from 'react-dom'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import InitialSettingsProvider from '../../shared/components/setup/InitialSettingsProvider'
import BaseLayout from '../../shared/components/BaseLayout'
import PageHeader from './components/PageHeader'
import CaseReviewTable from './components/CaseReviewTable'
import ReduxInit from '../../shared/components/setup/ReduxInit'

import rootReducer, { updateIndividualsByGuid, updateFamiliesByGuid } from './reducers/rootReducer'

import './casereview.css'

class CaseReviewPage extends React.Component
{
  render = () => {
    return <BaseLayout {...this.props}>
      <span>
        <PageHeader {...this.props} />
        <CaseReviewTable {...this.props} />
      </span>
    </BaseLayout>
  }
}

// wrap top-level component so that redux state is passed in as props
const mapStateToProps = ({ user, project, familiesByGuid, individualsByGuid, familyGuidToIndivGuids }) => {
  return {
    user,
    project,
    familiesByGuid,
    individualsByGuid,
    familyGuidToIndivGuids,
  }
}

const mapDispatchToProps = dispatch => bindActionCreators({
  updateIndividualsByGuid,
  updateFamiliesByGuid,
}, dispatch)

const CaseReviewPageWrapper = connect(mapStateToProps, mapDispatchToProps)(CaseReviewPage)

// render top-level component
ReactDOM.render(
  <InitialSettingsProvider>
    <ReduxInit storeName="CaseReview" rootReducer={rootReducer}>
      <CaseReviewPageWrapper />
    </ReduxInit>
  </InitialSettingsProvider>,
  document.getElementById('reactjs-root'),
)